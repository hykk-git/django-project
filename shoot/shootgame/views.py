from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import *
from .serializers import *
import random
import time
import uuid
from django.db import connection

class OutFrameView(TemplateView):
    template_name = "out_frame.html"

class FrameView(TemplateView):
    template_name = "frame.html"

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=False, methods=['post'])
    def create_player(self, request):
        Player.objects.all().delete()
        Enemy.objects.all().delete()
        Bullet.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='shootgame_enemy'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='shootgame_bullet'")

        player = Player.create_player()
        return Response({"message": "Game Start", "player_id": player.id})

    @action(detail=False, methods=['post'])
    def fire(self, request):
        player = Player.objects.first()
        if not player:
            return Response({"error": "Player not found"}, status=400)

        try:
            angle = int(request.data.get('angle'))
            print(f"Received fire request with angle: {angle}")  
        except (TypeError, ValueError):
            print("Invalid angle received!")  
            return Response({"error": "Invalid angle value"}, status=400)

        if Bullet.objects.count() >= 3:
            oldest_bullet = Bullet.objects.earliest('created')
            print(f"Deleting oldest bullet: {oldest_bullet.id}")
            oldest_bullet.delete()

        bullet = player.fire(angle)
        if not bullet:
            print("Bullet creation failed!")  
            return Response({"error": "Bullet could not be created"}, status=400)

        print(f"Bullet {bullet.id} created at ({bullet._coo_x}, {bullet._coo_y})") 
        return Response(BulletSerializer(bullet).data)

class EnemyViewSet(viewsets.ModelViewSet):
    queryset = Enemy.objects.all()
    serializer_class = EnemySerializer

    @action(detail=False, methods=['post'])
    def spawn(self, request):
        time.sleep(random.uniform(4, 6)) 
        enemy = Enemy.create_enemy()
        return Response(EnemySerializer(enemy).data)

    @action(detail=False, methods=['post'])
    def move(self, request):
        for enemy in Enemy.objects.all():
            enemy.move()

            if enemy.hit_bottom():
                print(f"Enemy {enemy.id} hit bottom!") 
                enemy.broke()

        return Response({"message": "Enemies moved"})

class BulletViewSet(viewsets.ModelViewSet):
    queryset = Bullet.objects.all()
    serializer_class = BulletSerializer
    lookup_field = "id"

    @action(detail=False, methods=['post'])
    def move(self, request):
        bullets = Bullet.objects.all()
        enemies = Enemy.objects.all()
        
        for bullet in bullets:
            bullet.move()

            for enemy in enemies:
                if bullet.hit_enemy(enemy):
                    print(f"Bullet {bullet.id} hit Enemy {enemy.id}")  
                    bullet.broke()
                    enemy.broke()
                    
                    player = Player.objects.first()
                    if player:
                        return Response({
                            "message": f"Bullet {bullet.id} hit Enemy {enemy.id}",
                            "score": player.score,
                            "life": player.life
                        })

        return Response({"message": "Bullets moved"})



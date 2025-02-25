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
    def get_player(self, request):
        Player.objects.all().delete()
        BoxEnemy.objects.all().delete()
        Bullet.objects.all().delete()

        player = Player.get_player()
        return Response({"message": "Game Start", "player_id": player.id})

    @action(detail=False, methods=['post'])
    def fire(self, request):
        player = Player.objects.first()
        if not player:
            return Response({"error": "Player not found"}, status=400)

        try:
            angle = int(request.data.get('angle'))  
        except (TypeError, ValueError):
            print("Invalid angle received!")  
            return Response({"error": "Invalid angle value"}, status=400)

        bullet = player.fire(angle)
        if not bullet:
            print("Bullet creation failed!")  
            return Response({"error": "Bullet could not be created"}, status=400)

        return Response(BulletSerializer(bullet).data)
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        player = Player.objects.first()
        if not player:
            return Response({"error": "Player not found"}, status=400)

        return Response({
            "score": player.score,
            "life": player.life,
            "game_over": player.game_over
        })

class BoxEnemyViewSet(viewsets.ModelViewSet):
    queryset = BoxEnemy.objects.all()
    serializer_class = BoxEnemySerializer

    @action(detail=False, methods=['post'])
    def spawn(self, request):
        enemy = BoxEnemy.create_enemy()
        time.sleep(random.uniform(3, 5)) 
        return Response(BoxEnemySerializer(enemy).data)

    @action(detail=False, methods=['post'])
    def move(self, request):
        for enemy in BoxEnemy.objects.all():
            enemy.move()

            if enemy.hit_bottom():
                enemy.broke()

        return Response({"message": "Enemies moved"})

class BulletViewSet(viewsets.ModelViewSet):
    queryset = Bullet.objects.all()
    serializer_class = BulletSerializer
    lookup_field = "id"

    @action(detail=False, methods=['post'])
    def move(self, request):
        bullets = Bullet.objects.all()
        enemies = BoxEnemy.objects.all()
        
        for bullet in bullets:
            bullet.move()

            for enemy in enemies:
                if bullet.hit_enemy(enemy):
                    bullet.broke()
                    enemy.broke()
                    
                    player = Player.objects.first()
                    return Response({
                            "message": f"Bullet {bullet.id} hit Enemy {enemy.id}",
                            "score": player.score,
                            "life": player.life
                        })
                        
        return Response({"message": "Bullets moved"})



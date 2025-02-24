from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import *
from .serializers import *
import random
import time
import uuid

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

        player = Player.create_player()
        # return Response({"message": "Player created"})
        return Response({"message": "Game Start", "player_id": player.id})
    
    @action(detail=False, methods=['post'])
    def fire(self, request):
        player = Player.objects.first()

        angle = int(request.data.get('angle'))
        bullet = player.fire(angle)

        return Response(BulletSerializer(bullet).data)

class EnemyViewSet(viewsets.ModelViewSet):
    queryset = Enemy.objects.all()
    serializer_class = EnemySerializer

    @action(detail=False, methods=['post'])
    def spawn(self, request):
        time.sleep(random.uniform(1, 3))
        enemy = Enemy.create_enemy()
        return Response(EnemySerializer(enemy).data)

    @action(detail=False, methods=['post'])
    def move(self, request):
        for enemy in Enemy.objects.all():
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
        for bullet in Bullet.objects.all():
            # bx, by = bullet.move()
            # print("bullet 위치: ", bx, by)
            bullet.move()
            bullet.reflex()

            enemies = Enemy.objects.all()
            for enemy in enemies:
                # ex, ey = enemy.move()
                # print("enemy 위치: ", ex, ey)
                if bullet.hit_enemy(enemy): 
                    bullet.broke()
                    enemy.broke()
                    break  

        return Response({"message": "Bullets moved"})

    # @action(detail=True, methods=['post'])
    # def reflex(self, request, id=None):
    #     try:
    #         bullet = Bullet.objects.get(id=id)
    #         bullet.reflex()
    #         return Response(BulletSerializer(bullet).data)
    #     except Bullet.DoesNotExist:
    #         return Response({"error": "Bullet not found"}, status=404)

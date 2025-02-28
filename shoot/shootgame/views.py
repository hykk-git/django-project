from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import *
from .serializers import PlayerSerializer, BulletSerializer
import random
import time

class OutFrameView(TemplateView):
    template_name = "out_frame.html"

class FrameView(TemplateView):
    template_name = "frame.html"

class PlayerView(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
        
    @action(detail=False, methods=['post'])
    def fire(self, request):
        player = Player.objects.first()
        if not player:
            return Response({"error": "Player not found"}, status=400)

        angle = int(request.data.get('angle'))
        bullet = player.fire(angle)
        if not bullet: 
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

class GameView(viewsets.ViewSet):
    ctr = CreateObject()

    def create(self, request, *args, **kwargs):
        player = Player.start_player()
        enemy = self.ctr.spawn(Enemy)
        return Response({"message": "Game Start", "player_id": player.id})
    
    @action(detail=False, methods=['post'])
    def spawn(self, request):
        enemy_data = self.ctr.spawn_enemy()
        time.sleep(random.uniform(3, 5)) 
        return Response(enemy_data)

    @action(detail=False, methods=['post'])
    def tick(self, request):
        game_state = self.ctr.update_tick()
        return Response(game_state)

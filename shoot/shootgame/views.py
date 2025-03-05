from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import *
from .serializers import *
import random
import time
from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


class OutFrameView(TemplateView):
    template_name = "out_frame.html"

class GameObjectsView(View):
    def get(self, request, *args, **kwargs):
        bullets = [bullet.aabb() for bullet in Bullet.objects.all()]
        enemies = [enemy.aabb() for enemy in Enemy.objects.all()]
        walls = [
            LeftWall.objects.first().aabb(), 
            RightWall.objects.first().aabb()
        ]
        ground = [Bottom.objects.first().aabb()]

        return JsonResponse({
            "bullets": bullets,
            "enemies": enemies,
            "walls": walls,
            "ground": ground
        })

@method_decorator(csrf_exempt, name='dispatch')
class FireBulletView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            angle = data.get("angle", 90)  
            angle = max(-90, min(90, angle)) 

            gun, _ = Gun.objects.get_or_create(
                defaults={"__point_x": GameArea.objects.first().__width // 2, "__point_y": GameArea.objects.first().__height - 50}
            )
            gun.fire(angle)

            return JsonResponse({"status": "success", "message": f"Bullet fired at {angle} degrees!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

class UpdateGameView(View):
    def get(self, request, *args, **kwargs):
        bullets = Bullet.objects.all()
        enemies = Enemy.objects.all()
        walls = [LeftWall.objects.first(), RightWall.objects.first(), Bottom.objects.first()]

        for bullet in bullets:
            bullet.update()
        for enemy in enemies:
            enemy.update()

        return JsonResponse({"status": "success", "message": "Game updated!"})

class GameFrameView(TemplateView):
    template_name = "frame.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_area = GameArea.objects.first()
        context["game_area"] = game_area
        return context
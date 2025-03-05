from django.urls import path
from .views import GameObjectsView, FireBulletView, GameFrameView, OutFrameView, UpdateGameView

urlpatterns = [
    path("game_objects/", GameObjectsView.as_view(), name="game_objects"),
    path("fire_bullet/", FireBulletView.as_view(), name="fire_bullet"),
    path("update_game/", UpdateGameView.as_view(), name="update_game"),
    path("frame/", GameFrameView.as_view(), name="frame"),
    path("out_frame/", OutFrameView.as_view(), name="out_frame"),
]
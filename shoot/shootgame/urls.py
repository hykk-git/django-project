from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'game', GameView, basename='game')
router.register(r'player', PlayerView, basename= 'player')
urlpatterns = [
    path('', include(router.urls)),
    path('game/start/', GameView.as_view({'post': 'start'}), name="game-start"),
    path('game/spawn/', GameView.as_view({'post': 'spawn'}), name="enemy-spawn"),
    path('game/tick/', GameView.as_view({'post': 'tick'}), name="game-tick"),
    path('player/start/', PlayerView.as_view({'post': 'start_player'}), name="player-start"),
    path('player/fire/', PlayerView.as_view({'post': 'fire'}), name="player-fire"),
    path('player/status/', PlayerView.as_view({'get': 'status'}), name="player-status"),
    path('home/', OutFrameView.as_view(), name="out_frame"), 
    path('frame/', TemplateView.as_view(template_name="frame.html"), name="frame"),
]
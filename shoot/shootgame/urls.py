from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from .views import *

router = DefaultRouter()
router.register(r'enemies', EnemyViewSet)
router.register(r'bullets', BulletViewSet)
router.register(r'player', PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/player/', PlayerViewSet.as_view({'post': 'get_player'}), name = "player-create"),
    path('player/fire/', PlayerViewSet.as_view({'post': 'fire'}), name = "player-fire"),
    path('enemies/spawn/', EnemyViewSet.as_view({'post': 'spawn'}), name = "enemy-spawn"),
    path('home/', OutFrameView.as_view(), name="out_frame"), 
    path('frame/', TemplateView.as_view(template_name="frame.html"), name = "frame"), 
]
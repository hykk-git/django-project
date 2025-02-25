from rest_framework import serializers
from .models import *

class BoxEnemySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxEnemy
        fields = '__all__'


class BulletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bullet
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
from django.db import models
import math
import random

class Config:
    FRAME_WIDTH = 600
    FRAME_HEIGHT = 800
    LIFE = 3
    SCORE = 0
    MAX_BULLET = 3
    BULLET_SIZE = 10
    ENEMY_SIZE = 50

class Player(models.Model):
    id = models.CharField(primary_key=True, default="1", max_length=10, editable=False)

    # Unit 참조
    def fire(self, angle):
        return Unit.create_bullet(angle)

class Unit(models.Model):
    __number = models.CharField(max_length=100, blank=True, null=True)
    __created = models.DateTimeField(auto_now_add=True)
    __point_x = models.IntegerField()
    __point_y = models.IntegerField()
    __speed = models.IntegerField(default=100)
    __angle = models.IntegerField(default=0)
    __size = models.IntegerField()

    @property
    def point(self):
        return self.__point_x, self.__point_y

    @point.setter
    def coo(self, val):
        self.__point_x, self.__point_y = val
    
    def broke(self):
        pass

    def move(self):
        self.__point_x += self.__speed * math.sin(math.radians(self.__angle))
        self.__point_y -= self.__speed * math.cos(math.radians(self.__angle))

    class meta:
        abstract = True

class Enemy(Unit):
    def broke(self):
        # 부모 의존성
        super().broke()

class Bullet(Unit):
    def broke(self):
        # 부모 의존성
        super().broke()

class CreateObject:
    def spawn(self, enemy):
        return enemy.objects.create()

class ControlObject:
    def isCollision(self, ob1, ob2):
        x1, y1 = ob1.coo
        x2, y2 = ob2.coo
        rad1 = ob1.size
        rad2 = ob2.size
        return (x2-x1)^2+(y2-y1)^2 <= (+rad2)^2 
    
class PlayerInfo:
    __score = models.IntegerField(default=0)
    __life = models.IntegerField(default=3)
    player = models.OneToOneField(Player, on_delete=models.CASCADE)

    def player_start(self):
        Player.objects.all().delete()

        player, _ = Player.objects.get_or_create(id=1, defaults={"name": "Player1"})
        return player
    
    def update(self):
        pass

    def lose_life(self, val):
        self._life -= val
        self.save()

    def gain_score(self, val):
        self._score += val
        self.save()
    
    

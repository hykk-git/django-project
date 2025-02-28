from django.db import models
import math
import random

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
    
    def broke(self):
        self.delete()

    def move(self, angle):
        pass

    def isCollision(self, ob1, ob2):
        x1, y1 = ob1.__coo
        x2, y2 = ob2.__coo
        rad1 = ob1.__size
        rad2 = ob2.__size
        return (x2-x1)^2+(y2-y1)^2 <= (rad1+rad2)^2 

    class meta:
        abstract = True

class Enemy(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    def move(self, angle):
        self.__point_y += self.__speed * math.sin(math.radians(angle))
    
class Bullet(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    def move(self, angle):
        self.__point_x += self.__speed * math.sin(math.radians(angle))
        self.__point_y -= self.__speed * math.cos(math.radians(angle))

class Player(models.Model):
    id = models.CharField(primary_key=True, default="1", max_length=10, editable=False)
    bullet = models.ForeignKey(Bullet, on_delete=models.CASCADE)

    def fire(self, angle):
        current_bullet = CreateObject.spawn(self.bullet)
        current_bullet.move(angle)

class CreateObject:
    def spawn(self, enemy):
        return enemy.objects.create()
    
class PlayerInfo(models.Model):
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
        self.__life -= val
        self.save()

    def gain_score(self, val):
        self.__score += val
        self.save()
    
    

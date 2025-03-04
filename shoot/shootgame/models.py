from django.db import models
import math
import random

class GameObject:
    class Meta:
        abstract = True

class Visible(GameObject):
    __point_x = models.IntegerField()
    __point_y = models.IntegerField()
    __height = models.IntegerField()
    __width= models.IntegerField()

    class Meta:
        abstract = True

class NonVisible(GameObject):
    class Meta:
        abstract = True

class Collisible(Visible):
    __speed = models.IntegerField()
    __angle = models.IntegerField()

    def isCollision(self, unit):
        x1, y1 = self.__point_x, self.__point_y

        # point 의존
        x2, y2 = unit.__point_x, unit.__point_y
        return (x2-x1)^2+(y2-y1)^2 <= (x1+x2)^2
    
    def move(self):
        pass

    class Meta:
        abstract = True

class PlayerStatus(NonVisible):
    score = models.IntegerField()
    life = models.IntegerField()

    def update():
        pass

    class Meta:
        abstract = True

class Gun(Visible):
    max_bullet = 3

    def fire(self, angle):
        Bullet_set.create_bullet(angle)

class Bullet(Collisible):
    gun = models.ForeignKey(Gun)

    def create_bullet(self, angle):
        return Bullet.objects.create(
            number=str(Bullet.objects.count()+1),
            __point_x=self.__width//2, # 중앙 생성
            __point_y=self.__height,
            __angle=angle
        )
    
    def move(self):
        self.__coo_x += self.__speed * math.sin(math.radians(self.__angle))
        self.__coo_y -= self.__speed * math.cos(math.radians(self.__angle))
        self.save()

class Enemy(Collisible):
    def move(self):
        self.__point_y += self.__speed
        self.save()


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

class Collapsible(Visible):
    __speed = models.IntegerField()
    __angle = models.IntegerField()

    def isCollision(self, unit):
        # 충돌을 확인하라
        x1, y1 = self.__point_x, self.__point_y

        # point 의존
        x2, y2 = unit.point_x, unit.point_y
        return (x2-x1)^2+(y2-y1)^2 <= (x1+x2)^2
    
    def move(self):
        pass
    
    def broke(self):
        pass

    class Meta:
        abstract = True

class PlayerStatus(NonVisible):
    status_val = models.IntegerField()
    def update(self, effect):
        self.status_val += effect
    
    class Meta:
        abstract = True

class Gun(Visible):
    max_bullet = models.IntegerField(default=3)

    def fire(self, angle):
        Bullet.create_bullet(angle)

class Bullet(Collapsible):
    gun = models.ForeignKey(Gun)

    @classmethod
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

    def broke(self):
        # if 벽일 때, else enemy일 때...
        pass

class Enemy(Collapsible):
    spawn_pos = models.CharField()

    @classmethod
    def create_enemy(self, angle):
        return Enemy.objects.create(
            number=str(Bullet.objects.count()+1),
            __point_x=random.choice(self.spawn_pos),
            __point_y=self.__height,
            __angle=angle
        )
    
    def move(self):
        self.__point_y += self.__speed
        self.save()
    
    def broke(self):
        #if 바닥일 때
        pass

class Score(PlayerStatus):
    pass

class Life(PlayerStatus):
    pass
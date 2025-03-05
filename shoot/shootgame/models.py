from django.db import models
import math
import random
from overrides import overrides

class GameObject:
    __name = models.CharField()

    @property
    def name(self):
        return self.name
    class Meta:
        abstract = True

class Visible(GameObject):
    __point_x = models.IntegerField()
    __point_y = models.IntegerField()

    @property
    def point(self):
        return self.__point_x, self.__point_y
    
    def update(self):
        # 자기 상태 업데이트(이동)
        pass

    class Meta:
        abstract = True

class Effect(GameObject):
    def activate(self):
        # 점수나 life, 반사 효과 활성화
        pass
    
    class Meta:
        abstract = True

class Collidable(Visible):
    # 충돌하는 객체들은 속도가 있음(움직임)
    __speed = models.IntegerField()

    def isCollision(self, unit):
        pass

    class Meta:
        abstract = True

class Gun(Visible):
    max_bullet = models.IntegerField(default=3)

    @overrides
    def update(self):
        x, y = Walls.point
        self.__point_x, self.__point_y = x//2, y
        self.save()
     
    def fire(self, angle):
        if Bullet.objects.count() >= self.max_bullet:
            Bullet.objects.last().delete()
        
        Bullet.create_bullet(angle)

class Bullet(Collidable):
    __angle = models.IntegerField()
    gun = models.ForeignKey(Gun)

    @classmethod
    def create_bullet(self, angle):
        return Bullet.objects.create(
            number=str(Bullet.objects.count()+1),
            __point_x=self.__width//2, # 중앙 생성
            __point_y=self.__height,
            __angle=angle
        )
    
    @overrides
    def isCollision(self, unit):
        x1, y1 = self.__point_x, self.__point_y
        x2, y2 = unit.point
        return (x2-x1)^2+(y2-y1)^2 <= (x1+x2)^2

    @overrides
    def update(self):
        x, y = self.__point_x, self.__point_y
        x += self._speed * math.sin(math.radians(self._angle))
        y -= self._speed * math.cos(math.radians(self._angle))
        self.save()
    
    def reflex(self):
        temp_angle = self.__angle
        self.__angle = -temp_angle

class Enemy(Collidable):
    spawn_pos = models.CharField()

    @classmethod
    def create_enemy(self, angle):
        return Enemy.objects.create(
            number=str(Bullet.objects.count()+1),
            __point_x=random.choice(self.spawn_pos),
            __point_y=self.__height,
            __angle=angle
        )
    
    @overrides
    def isCollision(self, unit):
        x1, y1 = self.__point_x, self.__point_y
        x2, y2 = unit.point
        return (x2-x1)^2+(y2-y1)^2 <= (x1+x2)^2

        # view에 가서 isColl->effect 호출 

    @overrides
    def update(self):
        self.__point_y += self.__speed
        self.save()

class Walls(Visible):
    height = models.IntegerField(default=800) 
    width = models.IntegerField(default=600)

    def update(self):
        self.__point_x, self.__point_y = 0, self.width

class reflex(Effect):
    # 충돌시 반사해라

    @overrides
    def activate(self, unit):
        unit.reflex()

class Score(Effect):
    status = models.IntegerField(default=0)

    @overrides
    def activate(self):
        self.status += 1

class Life(Effect):
    status = models.IntegerField(default=3)

    @overrides
    def activate(self):
        self.status -= 1
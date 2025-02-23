from django.db import models
from abc import ABC, abstractmethod
import math
import uuid
import random

class Player(models.Model):
    """
    Bullet 객체에게 총알 생성 요청 보내는 객체
    """
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _score = models.IntegerField(default=0)
    _life = models.IntegerField(default=3)
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, val):
        self._score += val

    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, val):
        self._life += val

    def reset(self):
        self._score = 0
        self._life = 3
        self.save()

    @classmethod
    def create_player(cls):
        player, created = cls.objects.get_or_create(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            defaults={"name": "Player1"}
        )
        if created:
            print("Player 생성 완료:", player)
        else:
            print("Player 존재:", player)
        return player
    
    def fire(self, angle):
        if self.life <= 0:
            return None
            
        if Bullet.objects.count() >= 3:
            Bullet.objects.first().delete()

        bullet = Bullet.objects.create(
            number=str(uuid.uuid4()),
            _coo_x=300,
            _coo_y=750,
            _angle=angle
        )
        return bullet
    
class Unit(models.Model):
    """
    게임 내 필요한 객체들을 생성하는 추상 클래스
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    _coo_x = models.IntegerField()
    _coo_y = models.IntegerField()

    @property
    def coo(self):
        return self._coo_x, self._coo_y

    @coo.setter
    def coo(self, val):
        self._coo_x, self._coo_y = val, val

    def move(self):
        pass

    def broke(self):
        pass

    class Meta:
        abstract = True


class Enemy(Unit):
    _speed = models.IntegerField(default=5)

    @classmethod
    def create_enemy(cls):
        spawn_positions = [50, 150, 250, 350, 450]  
        spawn_x = random.choice(spawn_positions)
        return cls.objects.create(
            number=str(uuid.uuid4()),
            _coo_x=spawn_x,
            _coo_y=0
        )

    def move(self):
        self._coo_y += self._speed
        self.save()

    def has_hit_bottom(self, screen_height=800):
        return self._coo_y >= screen_height

    def broke(self):
        player = Player.objects.first()
        player.life(-1)
        player.save()
        self.delete()

class Bullet(Unit):
    _angle = models.IntegerField()
    _speed = models.IntegerField(default=100)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        self._angle = val
        
    def move(self):
        self._coo_x += self._speed * math.cos(math.radians(self._angle))
        self._coo_y -= self._speed * math.sin(math.radians(self._angle))
        
        self.save()

    def reflex(self):
        if self._coo_x <= 0 or self._coo_x >= 600:
            self._angle = 180 - self._angle 

        if self._coo_y <= 0:
            self._angle = -self._angle

        self.save()

    def has_hit_target(self, enemy):
        return (
            abs(self._coo_x - enemy._coo_x) < 30 and
            abs(self._coo_y - enemy._coo_y) < 30
        )

    def broke(self):
        player = Player.objects.first()
        player.score(1)
        player.save()
        self.delete()
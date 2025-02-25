from django.db import models
import math
import uuid
import random

class Player(models.Model):
    """
    Bullet 객체에게 총알 생성 요청 보내는 객체
    """
    name = models.CharField(max_length=100)
    id = models.CharField(primary_key=True, default="1", max_length=10, editable=False)
    _score = models.IntegerField(default=0)
    _life = models.IntegerField(default=3)
    _game_over = models.BooleanField(default=False)

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

    @classmethod
    def create_player(cls):
        player, created = cls.objects.get_or_create(
            id=1,
            defaults={"name": "Player1"}
        )
        return player
    
    def fire(self, angle):
        if self.life <= 0:
            return None
            
        if Bullet.objects.count() >= 3:
            Bullet.objects.last().delete()
            
        bullet = Bullet.objects.create(
            number=int(Bullet.objects.count()+1),
            _coo_x=300,
            _coo_y=750,
            _angle=angle
        )
        return bullet
    
    @property
    def game_over(self):
        return self._life == 0

class Unit(models.Model):
    """
    게임 내 필요한 객체들을 생성하는 추상 클래스
    """
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    _coo_x = models.IntegerField()
    _coo_y = models.IntegerField()
    _speed = models.IntegerField(default=100)

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
    @classmethod
    def create_enemy(cls):
        spawn_positions = [50, 150, 250, 350, 450]  
        spawn_x = random.choice(spawn_positions)
        return cls.objects.create(
            _coo_x=spawn_x,
            _coo_y=0,
            _speed = 10
        )

    def move(self):
        self._coo_y += 10
        self.save()
        return self._coo_x, self._coo_y 

    def hit_bottom(self):
        return self._coo_y >=800

    def broke(self):
        player = Player.objects.filter(id=1).first()
        player.life = -1
        player.save()
        self.delete()

class Bullet(Unit):
    _angle = models.IntegerField()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        self._angle = val
        
    def move(self):
        self._coo_x += 50 * math.sin(math.radians(self._angle))
        self._coo_y -= 50 * math.cos(math.radians(self._angle))

        if self._coo_y < 0 or self._coo_y > 800:
            print(f"Bullet {self.id} out of bounds")
            self.delete()
            return

        if self._coo_x <= 0 or self._coo_x >= 600:
            self._angle = -self._angle

        self.save()

    def hit_enemy(self, enemy):
        bullet_left = self._coo_x - 5
        bullet_right = self._coo_x + 5
        bullet_top = self._coo_y - 5
        bullet_bottom = self._coo_y + 5

        enemy_left = enemy._coo_x - 25
        enemy_right = enemy._coo_x + 25
        enemy_top = enemy._coo_y - 25
        enemy_bottom = enemy._coo_y + 25

        if not (bullet_right < enemy_left or bullet_left > enemy_right or
                bullet_bottom < enemy_top or bullet_top > enemy_bottom):
            return True
        return False

    def broke(self):
        player = Player.objects.first()
        player.score += 1
        player.save()
        self.delete()

        
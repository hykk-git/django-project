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
    name = models.CharField(max_length=100)
    id = models.CharField(primary_key=True, default="1", max_length=10, editable=False)
    _score = models.IntegerField(default=Config.SCORE)
    _life = models.IntegerField(default=Config.LIFE)

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, val):
        self._score += val
        self.save()

    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, val):
        self._life += val
        self.save()

    @classmethod
    def start_player(cls):
        player, _ = cls.objects.get_or_create(id=1, defaults={"name": "Player1"})
        return player

    def take_damage(self, val):
        self._life -= val
        self.save()

    def gain_score(self, val):
        self._score += val
        self.save()

    def fire(self, angle):
        if self.life <= 0:
            return None
            
        if Bullet.objects.count() >= Config.MAX_BULLET:
            Bullet.objects.last().delete()
            
        bullet = Bullet.objects.create(
            number=int(Bullet.objects.count()+1),
            _coo_x=Config.FRAME_WIDTH//2,
            _coo_y=Config.FRAME_HEIGHT,
            _angle=angle
        )
        return bullet
    
    @property
    def game_over(self):
        return self.life <= 0

class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    _created = models.DateTimeField(auto_now_add=True)
    _coo_x = models.IntegerField()
    _coo_y = models.IntegerField()
    _speed = models.IntegerField(default=100)

    class Meta:
        abstract = True

    @property
    def coo(self):
        return self._coo_x, self._coo_y

    @coo.setter
    def coo(self, val):
        self._coo_x, self._coo_y = val

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, val):
        self.speed = val

    def move(self):
        pass

    def broke(self):
        self.delete()

class BoxEnemy(Unit):
    @classmethod
    def create_enemy(cls):
        spawn_pos = [50, 150, 250, 350, 450]
        spawn_x = random.choice(spawn_pos)
        return cls.objects.create(_coo_x=spawn_x, _coo_y=0, _speed=10)

    def move(self):
        self._coo_y += 10
        self.save()
        return self._coo_x, self._coo_y

    def hit_bottom(self):
        return self._coo_y >= Config.FRAME_HEIGHT

    def broke(self):
        player = Player.start_player()
        player.take_damage(1)
        super().broke()

class Bullet(Unit):
    _angle = models.IntegerField()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        self._angle = val

    def move(self):
        self._coo_x += self._speed * math.sin(math.radians(self._angle))
        self._coo_y -= self._speed * math.cos(math.radians(self._angle))

        if self._coo_y < 0 or self._coo_y > Config.FRAME_HEIGHT:
            self.delete()

        if self._coo_x <= 0 or self._coo_x >= Config.FRAME_WIDTH:
            self._angle = -self._angle

        self.save()

    def hit_enemy(self, enemy):
        bull_x, bull_y = self.coo
        enemy_x, enemy_y = enemy.coo
        bull_sz = Config.BULLET_SIZE//2
        enemy_sz = Config.ENEMY_SIZE//2
        bullet_rect = (bull_x- bull_sz, bull_y - bull_sz, bull_x + bull_sz, bull_y + bull_sz)
        enemy_rect = (enemy_x - enemy_sz, enemy_y - enemy_sz, enemy_x + enemy_sz, enemy_y + enemy_sz)

        overlap_x = bullet_rect[2] >= enemy_rect[0] and bullet_rect[0] <= enemy_rect[2]
        overlap_y = bullet_rect[3] >= enemy_rect[1] and bullet_rect[1] <= enemy_rect[3]

        return overlap_x and overlap_y

    def broke(self):
        player = Player.start_player()
        player.gain_score(1)
        super().broke()

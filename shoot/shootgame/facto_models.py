from django.db import models
import math
import random

class GameObject(models.Model):
    class Meta:
        abstract = True

class Visible(GameObject):
    _point_x = models.IntegerField()
    _point_y = models.IntegerField()
    _height = models.IntegerField()
    _width = models.IntegerField()

    class Meta:
        abstract = True

class NonVisible(GameObject):
    class Meta:
        abstract = True

class PlayerStatus(NonVisible):
    status_val = models.IntegerField(default=3)

    def update(self, effect):
        self.status_val += effect
        self.save()

    class Meta:
        abstract = True

class Score(PlayerStatus):
    pass

class Life(PlayerStatus):
    def is_game_over(self):
        return self.status_val <= 0

class Collidable:
    def collide_with(self, other):
        pass
    
class CollisionHandler:

    @staticmethod
    def handle_collision(obj1, obj2):
        obj1.collide_with(obj2)
        obj2.collide_with(obj1)

class Collapsible(Visible, Collidable):
    _speed = models.IntegerField(default=5)
    _angle = models.IntegerField(default=0)

    def move(self):
        self._point_x += int(self._speed * math.sin(math.radians(self._angle)))
        self._point_y -= int(self._speed * math.cos(math.radians(self._angle)))
        self.save()

    def destroy(self):
        self.delete()

class Gun(Visible):
    max_bullets = models.IntegerField(default=3)

    def fire(self, angle):
        if self.bullets.count() < self.max_bullets:
            Bullet.objects.last().delete()
        self.bullets.create(_angle=angle, 
                            _point_x=self._point_x, 
                            _point_y=self._point_y)

class Bullet(Collapsible):
    gun = models.ForeignKey(Gun, related_name="bullets", on_delete=models.CASCADE)

    def move(self, screen_width):
        super().move()

        if self._point_x <= 0 or self._point_x >= screen_width:
            self._angle = -self._angle
            self.save()

    def collide_with(self, other):
        if isinstance(other, Enemy):
            other.destroy()
            self.destroy()
        elif isinstance(other, Wall):
            self._angle = -self._angle
            self.save()

class Enemy(Collapsible):
    spawn_positions = models.JSONField(default=list)

    @classmethod
    def create_enemy(cls, screen_width):
        x_pos = random.randint(0, screen_width)
        return cls.objects.create(
            _point_x=x_pos,
            _point_y=0,
            _speed=random.randint(2, 5)
        )

    def move(self, floor_y, life_status):
        self._point_y += self._speed
        if self._point_y >= floor_y:
            CollisionHandler.handle_collision(self, life_status)  # 충돌 처리
            self.destroy()
        self.save()

    def collide_with(self, other):
        if isinstance(other, Bullet):
            self.destroy()
        elif isinstance(other, Life):
            other.update(-1) 
            
class Wall(Collidable):
    def collide_with(self, other):
        if isinstance(other, Bullet):
            other._angle = -other._angle
            other.save()

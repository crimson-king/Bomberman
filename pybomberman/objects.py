import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Surface

from pybomberman import PPM
from pybomberman.shapes import Shape, Rectangle
from framework.scene import Node


class GameObject(Node):
    def __init__(self, shape: Shape, sprite: Sprite, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = shape
        self.sprite = sprite
        self.velocity = Vector2()

        self.speed = PPM * 2

    def draw(self, canvas: Surface, offset=(0, 0)):
        dest = Rect(self.sprite.rect).move(offset + self.position)
        canvas.blit(self.sprite.image, dest)

    def update(self, dt):
        if self.velocity == (0, 0):
            return

        self.velocity.normalize_ip()
        self.position += self.velocity * self.speed * dt


class PlayerSprite(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM * .5, PPM * .5))
        self.image.fill((0x88, 0x88, 0))
        self.rect = self.image.get_rect()


class Player(GameObject):
    def __init__(self, sprite=PlayerSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, PPM >> 1, PPM >> 1)
        super().__init__(shape, sprite, *args, **kwargs)


class WallSprite(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0, 0, 0xaa))
        self.rect = self.image.get_rect()


class Wall(GameObject):
    def __init__(self, sprite=WallSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, PPM, PPM)
        super().__init__(shape, sprite, *args, **kwargs)

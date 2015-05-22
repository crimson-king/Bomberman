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

        self.speed = 2

    def draw(self, canvas: Surface, offset=(0, 0)):
        dest = Rect(self.sprite.rect).move((offset + self.position) * PPM)
        canvas.blit(self.sprite.image, dest)

    def update(self, dt):
        if self.velocity == (0, 0):
            return

        self.velocity.normalize_ip()
        self.position += self.velocity * self.speed * dt


class WallSprite(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0, 0, 0xaa))
        self.rect = self.image.get_rect()


class PlayerSprite(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM * .5, PPM * .5))
        self.image.fill((0x88, 0x88, 0))
        self.rect = self.image.get_rect()


class Wall(GameObject):
    def __init__(self, sprite=WallSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)


class Bomb(GameObject):
    def __init__(self, owner: 'Player', board: 'Board', sprite=WallSprite(),
                 *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)
        self.owner = owner
        self.board = board

        self.range = owner.bomb_range
        self.time = 3

    def update(self, dt):
        self.time -= 3
        self.parent.remove_node(self)


class Player(GameObject):
    def __init__(self, sprite=PlayerSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, .5, .5)
        super().__init__(shape, sprite, *args, **kwargs)

        self.kills = 0
        self.bomb_range = 1
        self.speed_level = 0

    def spawn_bomb(self, world: 'World'):
        bomb = Bomb(self, None)
        bomb.position.x = self.position.x
        bomb.position.y = self.position.y
        world.bombs.add_node(bomb)
        print('bomb spawned!')

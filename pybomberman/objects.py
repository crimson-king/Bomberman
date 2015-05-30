"""All game objects"""
from itertools import repeat

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame import Surface

from pybomberman import PPM

from pybomberman.shapes import Shape, Rectangle
from framework.scene import Node

from random import randint

class GameObject(Node):
    """Standard game object class"""
    def __init__(self, shape: Shape, sprite: Sprite, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = shape
        self.sprite = sprite
        self.velocity = Vector2()

        self.speed = 2

    def draw(self, canvas: Surface, offset=(0, 0)):
        """Draws itself"""
        dest = Rect(self.sprite.rect).move((offset + self.position) * PPM)
        canvas.blit(self.sprite.image, dest)

    def update(self, dt):
        """Updates itself if it has moved"""
        if self.velocity == (0, 0):
            return

        self.velocity.normalize_ip()
        self.position += self.velocity * self.speed * dt


class WallSprite(Sprite):
    """Sprite of wall"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0, 0, 0xff))
        self.rect = self.image.get_rect()


class DestructibleWallSprite(Sprite):
    """Sprite of destructible wall"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((139,69,19))
        self.rect = self.image.get_rect()


class BombSprite(Sprite):
    """Sprite of bomb"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()


class FireSprite(Sprite):
    """Sprite of fire"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0xff, 0, 0))
        self.rect = self.image.get_rect()


class PlayerSprite(Sprite):
    """Sprite of player"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM * .5, PPM * .5))
        self.image.fill((0, 0xff, 0))
        self.rect = self.image.get_rect()


class PowerupSprite(Sprite):
    """Sprite of powerup."""
    def __init__(self, name):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.rect = self.image.get_rect()
        color = (100, 100, 100)
        if name == 0:
            color = (100, 0, 0)
        elif name == 1:
            color = (0, 100, 0)
        elif name == 2:
            color = (0, 0, 100)
        self.image.fill(color)


class Wall(GameObject):
    """Wall. Unbowed. Unbent. Unbroken."""
    def __init__(self, sprite=WallSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)


class DestructibleWall(GameObject):
    """Wall that can be destroyed"""
    def __init__(self, sprite=DestructibleWallSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)

    def destroy(self, world):
        """Destroys the wall and has a small chance of spawning powerup"""
        random_number = randint(0, 19)
        if random_number < 4:  # 20% that the powerup will spawn
            powerup = Powerup(self, random_number)  # bomb range - 0, amount - 1, speed - 2, immortality - 3
            powerup.position.x = self.position[0]
            powerup.position.y = self.position[1]
            world.destructible_walls.add_node(powerup)
        self.parent.remove_node(self)


class Powerup(GameObject):
    """Powerup class"""
    def __init__(self, world: 'World', name=None, *args, **kwargs):
        sprite = PowerupSprite(name)
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)
        self.world = world


class Fire(GameObject):
    """Fire class"""
    def __init__(self, owner: 'Player', sprite=FireSprite(), *args,
                 **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)
        self.owner = owner

        self.time = 1

    def update(self, dt):
        """Burn baby burn"""
        self.time -= dt
        if self.time <= 0:
            self.parent.remove_node(self)


class Bomb(GameObject):
    """Bomb class"""
    def __init__(self, owner: 'Player', world: 'World', sprite=BombSprite(),
                 *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)
        self.owner = owner
        self.world = world

        self.range = owner.bomb_range
        self.time = 3

    def update(self, delta_time):
        """Checks the time it has left to detonate"""
        self.time -= delta_time
        if self.time <= 0:
            self.detonate()
            self.parent.remove_node(self)

    def detonate(self):
        """Now I am become Death, the Destroyer of Worlds."""
        right = zip(
            range(int(self.position.x) + 1, self.world.width),
            repeat(int(self.position.y)))
        left = zip(
            range(int(self.position.x) - 1, -1, -1),
            repeat(int(self.position.y)))
        up = zip(
            repeat(int(self.position.x)),
            range(int(self.position.y) - 1, -1, -1))
        down = zip(
            repeat(int(self.position.x)),
            range(int(self.position.y) + 1, self.world.height)
        )
        here = int(self.position.x), int(self.position.y)
        for fields in [here], left, right, up, down:
            for field in fields:
                # check if bomb may be placed here
                if field[0] % 2 == 1 and field[1] % 2 == 1:  # wall
                    break

                self.spawn_fire(field)

    def spawn_fire(self, field):
        """Spawns fire objects"""
        fire = Fire(self.owner)
        fire.position.x = field[0]
        fire.position.y = field[1]
        self.world.bombs.add_node(fire)


class Player(GameObject):
    """Player class"""
    def __init__(self, sprite=PlayerSprite(), *args, **kwargs):
        shape = Rectangle(0, 0, .5, .5)
        super().__init__(shape, sprite, *args, **kwargs)

        self.kills = 0
        self.bomb_range = 1
        self.speed_level = 0
        self.bomb_amount = 1

    def spawn_bomb(self, world: 'World', position):
        """Places a bomb on player position"""
        bomb = Bomb(self, world)
        bomb.position.x = position[0]
        bomb.position.y = position[1]
        world.bombs.add_node(bomb)

"""All game objects"""
import os
import random
from itertools import repeat

from pygame.math import Vector2
import pygame
from pygame.sprite import Sprite
from pygame import Surface

from pybomberman import PPM, ASSETS_PATH
from pybomberman.animation import Animation
from pybomberman.shapes import Shape, Rectangle
from framework.scene import Node


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
        canvas.blit(self.sprite.image, (offset + self.position) * PPM)

    def update(self, delta_time):
        """Updates itself if it has moved"""
        if self.velocity == (0, 0):
            return

        self.velocity.normalize_ip()
        self.position += self.velocity * self.speed * delta_time


class GenericSprite(Sprite):
    """Sprite of powerup."""

    def __init__(self, filename=None, color=(127, 127, 127)):
        super().__init__()

        if filename:
            self.image = pygame.image.load(filename)
        else:
            self.image = pygame.Surface((PPM, PPM))
            self.image.fill(color)

        self.rect = self.image.get_rect()


class Wall(GameObject):
    """Wall. Unbowed. Unbent. Unbroken."""

    def __init__(self,
                 sprite=GenericSprite(os.path.join(ASSETS_PATH, 'wall.png')),
                 *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)


class DestructibleWall(GameObject):
    """Wall that can be destroyed"""

    def __init__(self,
                 sprite=GenericSprite(os.path.join(ASSETS_PATH, 'd_wall.png')),
                 *args, **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)

    def destroy(self, world):
        """Destroys the wall and has a chance of spawning powerup"""
        if random.random() < .9:  # 20% that the powerup will spawn
            powerup_cls = random.choice(
                [BombAmountPowerup, RangePowerup, SpeedPowerup])
            powerup = powerup_cls(self)  # bomb range - 0
            powerup.position.x = self.position[0]  # amount - 1
            powerup.position.y = self.position[1]  # speed - 2
            world.powerups.add_node(powerup)  # immortality - 3
        self.parent.remove_node(self)


class Powerup(GameObject):
    """Powerup class"""

    def __init__(self, world: 'World', sprite=GenericSprite(), *args,
                 **kwargs):
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)
        self.world = world

    def collect(self, player: 'Player'):
        """Raises an error."""
        raise NotImplementedError


class BombAmountPowerup(Powerup):
    """Powerup increasing the amount of bombs"""

    def __init__(self, world, *args, **kwargs):
        sprite = GenericSprite(os.path.join(ASSETS_PATH, 'bomb_powerup.png'))
        super().__init__(world, sprite, *args, **kwargs)

    def collect(self, player: 'Player'):
        """Gives a player an additional bomb to use"""
        player.bomb_amount += 1


class SpeedPowerup(Powerup):
    """Powerup that increases player's speed"""

    def __init__(self, world, *args, **kwargs):
        filepath = os.path.join(ASSETS_PATH, 'speed_powerup.png')
        sprite = GenericSprite(filepath)
        super().__init__(world, sprite, *args, **kwargs)

    def collect(self, player: 'Player'):
        """Increases player's speed"""
        player.speed_level += 1


class RangePowerup(Powerup):
    """Powerup that extends your fire"""

    def __init__(self, world, *args, **kwargs):
        filepath = os.path.join(ASSETS_PATH, 'range_powerup.png')
        sprite = GenericSprite(filepath)
        super().__init__(world, sprite, *args, **kwargs)

    def collect(self, player: 'Player'):
        """Extends range of player's bombs"""
        player.bomb_range += 1


class Fire(GameObject):
    """Fire class"""

    def __init__(self, owner: 'Player', *args, **kwargs):
        filepath = os.path.join(ASSETS_PATH, 'fire.png')
        sprite = GenericSprite(filepath)
        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, sprite, *args, **kwargs)
        self.owner = owner

        self.time = 1

    def update(self, delta_time):
        """Burn baby burn"""
        self.time -= delta_time
        if self.time <= 0:
            self.parent.remove_node(self)


class Bomb(GameObject):
    """Bomb class"""

    def __init__(self, owner: 'Player', world: 'World', *args, **kwargs):
        bomb_sheet = pygame.image.load(
            os.path.join(ASSETS_PATH, 'bomb_sheet.png'))
        self.animation = Animation(bomb_sheet, 3, 1, 1)

        shape = Rectangle(0, 0, 1, 1)
        super().__init__(shape, self.animation, *args, **kwargs)
        self.owner = owner
        self.world = world

        self.range = owner.bomb_range
        self.time = 3

    def update(self, delta_time):
        """Checks the time it has left to detonate"""
        self.animation.update(delta_time)

        self.time -= delta_time
        if self.time <= 0:
            self.detonate()

    def detonate(self):
        """Now I am become Death, the Destroyer of Worlds."""

        # remove bomb from world here to avoid circular detonates
        self.parent.remove_node(self)
        self.owner.bombs.remove(self)

        right = zip(
            range(int(self.position.x) + 1,
                  min(int(self.position.x) + 1 + self.range,
                      self.world.width)),
            repeat(int(self.position.y)))
        left = zip(
            range(int(self.position.x) - 1,
                  max(int(self.position.x) - 1 - self.range, -1), -1),
            repeat(int(self.position.y)))
        upward = zip(
            repeat(int(self.position.x)),
            range(int(self.position.y) - 1,
                  max(int(self.position.y) - 1 - self.range, -1), -1))
        down = zip(
            repeat(int(self.position.x)),
            range(int(self.position.y) + 1,
                  min(int(self.position.y) + 1 + self.range,
                      self.world.height))
        )
        here = int(self.position.x), int(self.position.y)
        for fields in [here], left, right, upward, down:
            for field in fields:
                # check if bomb may be placed here
                if field[0] % 2 == 1 and field[1] % 2 == 1:  # wall
                    break

                self.spawn_fire(field)

                collision = None
                for wall in self.world.destructible_walls:
                    if field == wall.position:
                        collision = wall
                        wall.destroy(self.world)
                        break

                if collision:
                    break

                for bomb in self.world.bombs:
                    if field == (int(bomb.position.x), int(bomb.position.y)) \
                            and self is not bomb:
                        bomb.detonate()

    def spawn_fire(self, field):
        """Spawns fire objects"""
        fire = Fire(self.owner)
        fire.position.x = field[0]
        fire.position.y = field[1]
        self.world.fire.add_node(fire)


class Player(GameObject):
    """Player class"""

    sheet_movement = pygame.image.load(
        os.path.join(ASSETS_PATH, 'player_sheet.png'))

    def __init__(self, *args, **kwargs):
        self.animation = Animation(Player.sheet_movement, 4, 4, .33)
        self.animation.update(0)
        shape = Rectangle(
            0, 0,
            self.animation.frame_width / PPM,
            self.animation.frame_height / PPM)

        super().__init__(shape, self.animation, *args, **kwargs)

        self.health = 1
        self.bomb_range = 1
        self.bomb_amount = 1
        self.speed_level = 0

        self.kills = 0

        self.bombs = []

    def spawn_bomb(self, world: 'World', position):
        """Places a bomb on player position"""

        if len(self.bombs) == self.bomb_amount:
            return

        bomb = Bomb(self, world)
        bomb.position.x = position[0] \
                          + .5 * (1 - bomb.animation.frame_width / PPM)
        bomb.position.y = position[1] \
                          + .5 * (1 - bomb.animation.frame_height / PPM)
        self.bombs.append(bomb)
        world.bombs.add_node(bomb)

    def hit(self):
        """Hits player."""
        self.health -= 1

    def update(self, delta_time):
        """Updates, animates, and stuff"""
        super().update(delta_time)

        if self.velocity.x > 0:
            self.animation.col = 3
        if self.velocity.x < 0:
            self.animation.col = 1

        if self.velocity.y > 0:
            self.animation.col = 0
        if self.velocity.y < 0:
            self.animation.col = 2

        if self.velocity != (0, 0):
            self.sprite.update(delta_time * self.speed)

        for bomb in self.bombs:
            if bomb.time <= 0:
                self.bombs.remove(bomb)

    @property
    def speed(self):
        """Returns speed"""
        return 1.5 + self.speed_level * .25

    @speed.setter
    def speed(self, value):
        """Sets speed"""
        pass

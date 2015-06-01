"""What a wonderful world."""
from itertools import product
import random

import pygame
from framework import input_manager, state_manager
from framework.core import Game
from framework.input import InitialAction
from framework.state import State
from framework.scene import NodeGroup
from pybomberman import PPM
from pybomberman import physics
from pybomberman.config import config
from pybomberman.controllers import HumanController
from pybomberman.objects import Wall, Player, DestructibleWall


class World(NodeGroup):
    """Contains node groups with objects"""

    def __init__(self, width: int, height: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = width
        self.height = height

        self.powerups = NodeGroup()
        self.add_node(self.powerups)

        self.walls = NodeGroup()
        self.add_node(self.walls)

        self.destructible_walls = NodeGroup()
        self.add_node(self.destructible_walls)

        self.bombs = NodeGroup()
        self.add_node(self.bombs)

        self.fire = NodeGroup()
        self.add_node(self.fire)

        self.players = NodeGroup()
        self.add_node(self.players)

        # at this positions walls must not be spawned
        player_space = (
            (0, 0), (0, 1), (1, 0),
            (width - 1, 0), (width - 1, 1), (width - 2, 0),
            (0, height - 1), (0, height - 2), (1, height - 1),
            (width - 1, height - 1), (width - 2, height - 1), (width - 1, height - 2)
        )

        for pos_x, pos_y in product(range(width), range(height)):
            if (pos_x, pos_y) in player_space:
                continue
            if pos_x % 2 == 1 and pos_y % 2 == 1:  # wall
                self.add_wall((pos_x, pos_y))
            else:
                if random.random() < .8:
                    self.add_destructible_wall((pos_x, pos_y))

    def add_wall(self, position):
        wall = Wall()
        wall.position.x = position[0]
        wall.position.y = position[1]
        self.walls.add_node(wall)

    def add_destructible_wall(self, position):
        wall = DestructibleWall()
        wall.position.x = position[0]
        wall.position.y = position[1]
        self.destructible_walls.add_node(wall)

    def add_player(self, *args, **kwargs) -> Player:
        player = Player(*args, **kwargs)

        left = player.shape.width * .5
        right = self.width - 1 + left
        top = player.shape.height * .5
        down = self.height - 1 + top

        players_count = len(self.players)
        if players_count == 0:
            position = left, top
        elif players_count == 1:
            position = right, down
        elif players_count == 2:
            position = left, down
        elif players_count == 3:
            position = right, top
        else:
            raise NotImplementedError('too many players')

        player.position.x = position[0]
        player.position.y = position[1]
        self.players.add_node(player)
        return player

    def draw(self, canvas, offset=(0, 0)):
        """Draws itself"""
        super().draw(canvas, offset)

    def update(self, dt):
        """Updates and sets collisions"""
        super().update(dt)

        for player in self.players:
            for wall in self.walls:
                physics.collides(player, wall, resolve=True)
            for d_wall in self.destructible_walls:
                physics.collides(player, d_wall, resolve=True)

            for powerup in self.powerups:
                if physics.collides(player, powerup, resolve=False):
                    powerup.collect(player)
                    self.powerups.remove_node(powerup)
            for fire in self.fire:
                if physics.collides(player, fire, resolve=False):
                    player.hit()

            if player.health <= 0:
                self.players.remove_node(player)


class GameState(State):
    """Game State"""

    def __init__(self):
        self.world = World(9, 9)
        self.world.position.x = \
            (config.resolution[0] / PPM - self.world.width) * .5
        self.world.position.y = \
            (config.resolution[1] / PPM - self.world.height) * .5

        self.controllers = [
            HumanController(self.world.add_player(), self.world)
            for _ in range(config.player_count)
        ]

        for controller in self.controllers:
            self.world.players.add_node(controller.player)

        self.escape_action = InitialAction()

    def resume(self):
        """Resumes the state of the game"""
        input_manager.map_action(pygame.K_ESCAPE, self.escape_action)

        for i, controller in enumerate(self.controllers):
            player_config = config.players[i]
            input_manager.map_action(
                player_config.key_binding.upward, controller.action_up)
            input_manager.map_action(
                player_config.key_binding.down, controller.action_down)
            input_manager.map_action(
                player_config.key_binding.left, controller.action_left)
            input_manager.map_action(
                player_config.key_binding.right, controller.action_right)
            input_manager.map_action(
                player_config.key_binding.action, controller.action_action)

        input_manager.reset()

    def pause(self):
        """Pauses the game"""
        input_manager.clear()

    def handle_input(self, event):
        """Handles user input"""
        input_manager.handle_input(event)

    def handle_draw(self, canvas):
        """Draws the game"""
        canvas.fill((0x33, 0x33, 0x33))
        self.world.draw(canvas)

    def handle_update(self, dt):
        """Updates the game, world and controllers"""
        if self.escape_action.active():
            state_manager.pop()

        for controller in self.controllers:
            controller.update(dt)

        self.world.update(dt)

        for controller in self.controllers:
            if controller.player.health <= 0:
                self.controllers.remove(controller)


if __name__ == '__main__':
    from framework.state import StateGameHandler

    state_manager.push(GameState())
    Game(handler=StateGameHandler()).start()
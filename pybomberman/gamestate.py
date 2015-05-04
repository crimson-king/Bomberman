import math

import pygame
from pygame.sprite import Group

from framework import input_manager

from framework.core import Game

from framework.input import InitialAction
from framework.state import State
from pybomberman import PPM
from pybomberman.configuration import configuration
from pybomberman.controllers import HumanController
from pybomberman.objects import Player, Wall
from pybomberman.utils import abs_ceil


class Board:
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.players = Group()
        self.walls = Group()
        for w in range(width >> 1):
            for h in range(height >> 1):
                wall = Wall()
                wall.rect.x = PPM * (2 * w + 1)
                wall.rect.y = PPM * (2 * h + 1)
                self.walls.add(wall)

    def draw(self, canvas):
        self.walls.draw(canvas)
        self.players.draw(canvas)

    def update(self, dt):
        self.players.update(dt)


class GameState(State):
    def __init__(self):
        # self.board = Group()
        self.board = Board(9, 9)

        self.controllers = [HumanController(Player())
                            for i in range(configuration.players)]

        for controller in self.controllers:
            self.board.players.add(controller.player)

        self.escape_action = InitialAction()

    def resume(self):
        input_manager.map_action(pygame.K_ESCAPE, self.escape_action)

        for i, controller in enumerate(self.controllers):
            input_manager.map_action(configuration.player_key_configs[i].up,
                                     controller.action_up)
            input_manager.map_action(configuration.player_key_configs[i].down,
                                     controller.action_down)
            input_manager.map_action(configuration.player_key_configs[i].left,
                                     controller.action_left)
            input_manager.map_action(configuration.player_key_configs[i].right,
                                     controller.action_right)

        input_manager.reset()

    def pause(self):
        input_manager.clear()

    def handle_input(self, event):
        input_manager.handle_input(event)

    def handle_draw(self, canvas):
        canvas.fill((0, 25, 0))
        self.board.draw(canvas)

    def handle_update(self, dt):
        if self.escape_action.active():
            state_manager.pop()

        for controller in self.controllers:
            controller.update(dt)

        self.board.update(dt)

        for player in self.board.players:
            player_center_x = player.rect.x + player.rect.width * .5
            player_center_y = player.rect.y + player.rect.height * .5
            for wall in self.board.walls:
                wall_center_x = wall.rect.x + wall.rect.width * .5
                wall_center_y = wall.rect.y + wall.rect.height * .5

                radius = (player.rect.width + wall.rect.width) * .5

                delta_x = player_center_x - wall_center_x
                delta_y = player_center_y - wall_center_y

                delta_sq = delta_x ** 2 + delta_y ** 2
                if delta_sq < radius ** 2:
                    angle = math.atan2(delta_y, delta_x) + math.pi * .5

                    dist = radius - math.sqrt(delta_sq)

                    player.rect.x += abs_ceil(math.sin(angle) * dist)
                    player.rect.y -= abs_ceil(math.cos(angle) * dist)


if __name__ == '__main__':
    from framework import state_manager
    from framework.state import StateGameHandler

    state_manager.push(GameState())
    Game(handler=StateGameHandler()).start()

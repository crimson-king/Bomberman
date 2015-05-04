import pygame
from pygame.sprite import Group

from pybomberman.controllers import HumanController

from framework.core import Game
from framework.input import InitialAction
from framework.state import State
from framework import input_manager
from pybomberman.configuration import configuration
from pybomberman.objects import Player


class GameState(State):
    def __init__(self):
        self.board = Group()

        self.controllers = [HumanController(Player())
                            for i in range(configuration.players)]

        for controller in self.controllers:
            self.board.add(controller.player)

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


if __name__ == '__main__':
    from framework import state_manager
    from framework.state import StateGameHandler

    state_manager.push(GameState())
    Game(handler=StateGameHandler()).start()

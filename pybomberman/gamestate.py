import pygame
from pygame.sprite import Group

from framework.core import Game
from framework.input import NormalAction, InitialAction
from framework.state import State
from pybomberman.objects import Player


class GameState(State):
    def __init__(self):
        self.player = Player()
        self.board = Group()
        self.board.add(self.player)

        self.escape_action = InitialAction()
        self.up_action = NormalAction()
        self.down_action = NormalAction()
        self.left_action = NormalAction()
        self.right_action = NormalAction()

    def resume(self):
        input_manager.map_action(pygame.K_ESCAPE, self.escape_action)
        input_manager.map_action(pygame.K_UP, self.up_action)
        input_manager.map_action(pygame.K_DOWN, self.down_action)
        input_manager.map_action(pygame.K_LEFT, self.left_action)
        input_manager.map_action(pygame.K_RIGHT, self.right_action)
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

        dx, dy = 0, 0

        dx += self.right_action.active() - self.left_action.active()
        dy -= self.up_action.active() - self.down_action.active()

        self.player.rect.move_ip(dx, dy)

        self.board.update(dt)


if __name__ == '__main__':
    from framework import state_manager, input_manager
    from framework.state import StateGameHandler

    state_manager.push(GameState())
    Game(handler=StateGameHandler()).start()

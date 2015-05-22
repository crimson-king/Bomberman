import pygame

from framework import input_manager, state_manager
from framework.core import Game
from framework.input import InitialAction
from framework.state import State
from pybomberman import PPM
from pybomberman.configuration import configuration
from pybomberman.controllers import HumanController
from pybomberman.objects import PlayerSprite, GameObject, Wall
from pybomberman.shapes import Rectangle
from framework.scene import NodeGroup


class Board(NodeGroup):
    def __init__(self, board_width: int, board_height: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.board_width = board_width
        self.board_height = board_height
        self.width = self.board_width * PPM
        self.height = self.board_height * PPM

        self.players = NodeGroup()
        self.walls = NodeGroup()
        self.add_node(self.walls)
        self.add_node(self.players)

        for w in range(board_width >> 1):
            for h in range(board_height >> 1):
                wall = Wall()
                wall.position.x = PPM * (2 * w + 1)
                wall.position.y = PPM * (2 * h + 1)
                self.walls.add_node(wall)

    def draw(self, canvas, offset=(0, 0)):
        super().draw(canvas, offset)

    def update(self, dt):
        self.players.update(dt)


class GameState(State):
    def __init__(self):
        self.board = Board(9, 9)
        self.board.position.x = \
            (configuration.resolution[0] - self.board.width) * .5
        self.board.position.y = \
            (configuration.resolution[1] - self.board.height) * .5

        self.controllers = [HumanController(PlayerSprite())
                            for i in range(configuration.players)]

        for controller in self.controllers:
            self.board.add_node(GameObject(shape=Rectangle(0, 0, 50, 50),
                                           sprite=controller.player))

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
        canvas.fill((0x33, 0x33, 0x33))
        self.board.draw(canvas)

    def handle_update(self, dt):
        if self.escape_action.active():
            state_manager.pop()

        for controller in self.controllers:
            controller.update(dt)

        self.board.update(dt)


if __name__ == '__main__':
    from framework.state import StateGameHandler

    state_manager.push(GameState())
    Game(handler=StateGameHandler()).start()

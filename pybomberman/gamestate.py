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
from pybomberman.objects import Wall, Player


class World(NodeGroup):
    def __init__(self, width: int, height: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = width
        self.height = height

        self.walls = NodeGroup()
        self.add_node(self.walls)

        self.bombs = NodeGroup()
        self.add_node(self.bombs)

        self.players = NodeGroup()
        self.add_node(self.players)

        for w in range(width >> 1):
            for h in range(height >> 1):
                wall = Wall()
                wall.position.x = 2 * w + 1
                wall.position.y = 2 * h + 1
                self.walls.add_node(wall)

    def draw(self, canvas, offset=(0, 0)):
        super().draw(canvas, offset)

    def update(self, dt):
        super().update(dt)

        for player in self.players:
            for wall in self.walls:
                physics.collides(player, wall, resolve=True)


class GameState(State):
    def __init__(self):
        self.world = World(9, 9)
        self.world.position.x = \
            (config.resolution[0] / PPM - self.world.width) * .5
        self.world.position.y = \
            (config.resolution[1] / PPM - self.world.height) * .5

        self.controllers = [HumanController(Player(), self.world)
                            for _ in range(config.player_count)]

        for controller in self.controllers:
            self.world.players.add_node(controller.player)

        self.escape_action = InitialAction()

    def resume(self):
        input_manager.map_action(pygame.K_ESCAPE, self.escape_action)

        for i, controller in enumerate(self.controllers):
            player_config = config.players[i]
            input_manager.map_action(
                player_config.key_binding.up, controller.action_up)
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
        input_manager.clear()

    def handle_input(self, event):
        input_manager.handle_input(event)

    def handle_draw(self, canvas):
        canvas.fill((0x33, 0x33, 0x33))
        self.world.draw(canvas)

    def handle_update(self, dt):
        if self.escape_action.active():
            state_manager.pop()

        for controller in self.controllers:
            controller.update(dt)

        self.world.update(dt)


if __name__ == '__main__':
    from framework.state import StateGameHandler

    state_manager.push(GameState())
    Game(handler=StateGameHandler()).start()

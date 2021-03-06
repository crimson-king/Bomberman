"""A controller"""
from framework.input import NormalAction, InitialAction
from pybomberman.objects import Player


class Controller:
    """Abstract controller"""
    def update(self, delta_time):
        """Abstract update"""
        pass


class HumanController(Controller):
    """Actual implementation of a controller"""
    def __init__(self, player: Player, world: 'World'):
        self.player = player
        self.world = world

        self.action_action = InitialAction()
        self.action_up = NormalAction()
        self.action_down = NormalAction()
        self.action_left = NormalAction()
        self.action_right = NormalAction()

    def update(self, delta_time):
        """Handles velocity and action"""
        self.player.velocity.x = \
            self.action_right.active() - self.action_left.active()
        self.player.velocity.y = \
            - (self.action_up.active() - self.action_down.active())

        if self.action_action.active():
            position = \
                int(self.player.position.x + self.player.shape.width * .5), \
                int(self.player.position.y + self.player.shape.height * .5)
            self.player.spawn_bomb(self.world, position)

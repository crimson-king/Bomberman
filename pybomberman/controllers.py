"""A controller"""
from framework.input import NormalAction, InitialAction
from pybomberman.objects import Player


class Controller:
    """Abstract controller"""
    def update(self, dt):
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

    def update(self, dt):
        """Handles velocity and action"""
        self.player.velocity.pos_x = \
            self.action_right.active() - self.action_left.active()
        self.player.velocity.pos_y = \
            - (self.action_up.active() - self.action_down.active())

        if self.action_action.active():
            position = \
                int(self.player.position.pos_x + self.player.shape.width * .5), \
                int(self.player.position.pos_y + self.player.shape.height * .5)
            self.player.spawn_bomb(self.world, position)

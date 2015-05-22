from framework.input import NormalAction, InitialAction
from pybomberman.objects import Player


class Controller:
    def update(self, dt):
        pass


class HumanController(Controller):
    def __init__(self, player: Player):
        self.player = player
        self.action_action = InitialAction()
        self.action_up = NormalAction()
        self.action_down = NormalAction()
        self.action_left = NormalAction()
        self.action_right = NormalAction()

    def update(self, dt):
        self.player.velocity.x = \
            self.action_right.active() - self.action_left.active()
        self.player.velocity.y = \
            - (self.action_up.active() - self.action_down.active())

        self.player.update(dt)

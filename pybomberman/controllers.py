from framework.input import NormalAction, InitialAction
from pybomberman.objects import PlayerSprite


class Controller:
    def update(self, dt):
        pass


class HumanController(Controller):
    def __init__(self, player: PlayerSprite):
        self.player = player
        self.action_action = InitialAction()
        self.action_up = NormalAction()
        self.action_down = NormalAction()
        self.action_left = NormalAction()
        self.action_right = NormalAction()

    def update(self, dt):
        dx, dy = 0, 0

        dx += self.action_right.active() - self.action_left.active()
        dy -= self.action_up.active() - self.action_down.active()

        self.player.rect.move_ip(dx, dy)

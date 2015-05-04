import pygame


class PlayerKeyConfiguration:
    def __init__(self,
                 action=pygame.K_SPACE,
                 up=pygame.K_UP,
                 down=pygame.K_DOWN,
                 left=pygame.K_LEFT,
                 right=pygame.K_RIGHT):
        self.action = action
        self.up = up
        self.down = down
        self.left = left
        self.right = right


class Configuration:
    players = 2
    # resolution = (...)
    # key bindings for each player = <tu po jakiejs liscie po 5 klawiszy>

    def __init__(self):
        self.player_key_configs = [PlayerKeyConfiguration()
                                   for i in range(self.players)]


configuration = Configuration()
"""class _Configuration:
        def __init__(self):
            self.players = 2

        def setplayers(self, i):
            self.players = i

    instance = None

    def __init__(self, arg):
        if not Configuration.instance:
            Configuration.instance = Configuration._Configuration()"""

import json

import pygame


class PlayerKeyConfiguration:
    def __init__(self, i,
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
        self.number = i


class Configuration:

    max_players = 4
    resolution = (960, 600)

    def __init__(self):
        file = open('settings.json')
        settings = json.load(file)
        self.player_key_configs = [PlayerKeyConfiguration(i, settings['p'+str(i)+'keys']['action'],
                                                          settings['p'+str(i)+'keys']['up'],
                                                          settings['p'+str(i)+'keys']['down'],
                                                          settings['p'+str(i)+'keys']['left'],
                                                          settings['p'+str(i)+'keys']['right'])
                                   for i in range(self.max_players)]

        self.players = settings['players']['amount']

configuration = Configuration()

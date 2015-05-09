import shelve
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
    # resolution = (...)
    # key bindings for each player = <tu po jakiejs liscie po 5 klawiszy>

    def __init__(self):
        shelf = shelve.open('shelf.db', writeback=True)
        self.player_key_configs = [PlayerKeyConfiguration(i, shelf['player'+str(i)+'action'],
                                                          shelf['player'+str(i)+'up'], shelf['player'+str(i)+'down'],
                                                          shelf['player'+str(i)+'left'], shelf['player'+str(i)+'right'])
                                   for i in range(self.max_players)]
        self.players = shelf['players']
        shelf.close()

configuration = Configuration()

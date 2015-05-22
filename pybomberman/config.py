import os
import json

import pygame

import pybomberman


class PlayerKeyBinding:
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


class PlayerConfig:
    def __init__(self, **kwargs):
        self.key_binding = PlayerKeyBinding(**kwargs['key_binding'])


class Config:
    def __init__(self, **kwargs):
        self.resolution = (960, 600)
        self.player_count = 2

        self.players = [PlayerConfig(**player_dict)
                        for player_dict in kwargs['players']]

_filename = 'config.json'

_MAX_PLAYERS = 4

_pybomberman_dirname = os.path.dirname(pybomberman.__file__)
_filepath = os.path.join(os.path.dirname(_pybomberman_dirname), _filename)
if os.path.exists(_filepath):
    with open(_filepath) as config_file:
        try:
            config = json.load(config_file)
        except ValueError as error:
            error.args += 'Invalid configuration file',
            raise
else:
    raise FileNotFoundError(
        'Could not find configuration file: {}'.format(_filepath))


config = Config(**config)

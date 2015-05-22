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

    def to_dict(self):
        return {'key_binding': self.key_binding.__dict__}


class Config:
    def __init__(self, **kwargs):
        self.player_count = kwargs['player_count']
        self.resolution = kwargs['resolution']

        self.players = [PlayerConfig(**player_dict)
                        for player_dict in kwargs['players']]

    def to_dict(self):
        return {'resolution': self.resolution,
                'player_count': self.player_count,
                'players': [p.to_dict() for p in self.players],
                }

    def save(self):
        with open(_filepath, mode='w+') as file_handle:
            json.dump(self.to_dict(), fp=file_handle, indent=4)

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

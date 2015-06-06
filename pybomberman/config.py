"""Configuration"""
import os
import json

import pygame

import pybomberman
# pylint: disable=no-member

class PlayerKeyBinding:
    """5 keys that player uses"""
    def __init__(self,
                 action=pygame.K_SPACE,
                 upward=pygame.K_UP,
                 down=pygame.K_DOWN,
                 left=pygame.K_LEFT,
                 right=pygame.K_RIGHT):
        self.action = action
        self.upward = upward
        self.down = down
        self.left = left
        self.right = right


class PlayerConfig:
    """Player configuration"""
    def __init__(self, **kwargs):
        self.key_binding = PlayerKeyBinding(**kwargs['key_binding'])

    def to_dict(self):
        """Returns dictionary out of keys"""
        return {'key_binding': self.key_binding.__dict__}


class Config:
    """Configuration class"""
    def __init__(self, **kwargs):
        self.player_count = kwargs['player_count']
        self.resolution = kwargs['resolution']
        self.players = [PlayerConfig(**player_dict)
                        for player_dict in kwargs['players']]

    def update(self, **kwargs):
        """Updates config"""
        self.player_count = kwargs['player_count']
        self.resolution = kwargs['resolution']
        self.players = [PlayerConfig(**player_dict)
                        for player_dict in kwargs['players']]

    def to_dict(self):
        """Returns dictionary out of configuration"""
        return {'resolution': self.resolution,
                'player_count': self.player_count,
                'players': [p.to_dict() for p in self.players]}

    def save(self):
        """Saves configuration in json"""
        with open(filepath, mode='w+') as file_handle:
            json.dump(self.to_dict(), fp=file_handle, indent=4)

# pylint: disable=invalid-name
# not constants

filename = 'config.json'

_MAX_PLAYERS = 4

pybomberman_dirname = os.path.dirname(pybomberman.__file__)
filepath = os.path.join(os.path.dirname(pybomberman_dirname), filename)
if os.path.exists(filepath):
    with open(filepath) as config_file:
        try:
            config = json.load(config_file)
        except ValueError as error:
            error.args += 'Invalid configuration file',
            raise
else:
    raise FileNotFoundError(
        'Could not find configuration file: {}'.format(filepath))


config = Config(**config)

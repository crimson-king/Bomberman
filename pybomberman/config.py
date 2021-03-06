"""Configuration"""
import os
import json

# pylint: disable=no-member
import pygame

import pybomberman


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

    def to_dict(self):
        """Returns dictionary out of configuration"""
        return {'resolution': self.resolution,
                'player_count': self.player_count,
                'players': [p.to_dict() for p in self.players]}

    def save(self):
        """Saves configuration in json"""
        with open(FILEPATH, mode='w+') as file_handle:
            json.dump(self.to_dict(), fp=file_handle, indent=4)


FILENAME = 'config.json'

PROJECT_DIRNAME = os.path.dirname(pybomberman.__file__)
FILEPATH = os.path.join(os.path.dirname(PROJECT_DIRNAME), FILENAME)

# not a constant
# pylint: disable=invalid-name

if os.path.exists(FILEPATH):
    with open(FILEPATH) as config_file:
        try:
            config = json.load(config_file)
        except ValueError as error:
            error.args += 'Invalid configuration file',
            raise
else:
    raise FileNotFoundError(
        'Could not find configuration file: {}'.format(FILEPATH))

config = Config(**config)

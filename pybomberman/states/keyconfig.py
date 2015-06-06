"""
This module implements functionality that allows user to view and change key
 mappings.
"""
__author__ = 'Tomasz Rzepka'
import pygame

from framework.ui import StageState, Button
from pybomberman.menu import Item
from pybomberman.config import config
from framework import state_manager

# pylint: disable=no-member
pygame.init()


class KeyConfigState(StageState):
    """
    This class implements State that allows user to view and change key
    mappings
    """
    def __init__(self):
        super().__init__()
        self.current_player = 0
        self.selecting_key = False

        self.player_button = Button('PLAYER <%d> KEYS' % (self.current_player + 1))
        self.player_button.on_click = self.on_click
        self.stage.add_node(self.player_button)

        self.action_button = Button('ACTION: ' + pygame.key.name(
                                    config.players[self.current_player].key_binding.action))
        self.stage.add_node(self.action_button)
        self.action_button.on_click = self.on_click

        self.up_button = Button('UP: ' + pygame.key.name(
                                config.players[self.current_player].key_binding.upward))
        self.stage.add_node(self.up_button)
        self.up_button.on_click = self.on_click

        self.down_button = Button('DOWN: ' + pygame.key.name(
                                  config.players[self.current_player].key_binding.down))
        self.stage.add_node(self.down_button)
        self.down_button.on_click = self.on_click

        self.left_button = Button('LEFT: ' + pygame.key.name(
                                  config.players[self.current_player].key_binding.left))
        self.stage.add_node(self.left_button)
        self.left_button.on_click = self.on_click

        self.right_button = Button('RIGHT: ' + pygame.key.name(
                                   config.players[self.current_player].key_binding.right))
        self.stage.add_node(self.right_button)
        self.right_button.on_click = self.on_click

        self.exit_button = Button('GO BACK')
        self.stage.add_node(self.exit_button)
        self.exit_button.on_click = self.on_click

    def select_key(self):
        """ Prepares key for new mapping """
        self.items[self.selected].text = \
            self.items[self.selected].text.rsplit(':', 1)[0]
        self.items[self.selected].text += ": <select key>"
        self.selecting_key = True

    def change_current_player(self):
        """ selects next available for which settings are being set """
        self.current_player = (
            (self.current_player + 1) % 4)
        self.player_button.text = "PLAYER <%d> KEYS" % (
            self.current_player + 1)
        self.update_keys()

    def update_keys(self):
        """ updates key names for key mappings for current player """
        self.action_button.text = 'Action: ' + pygame.key.name(
            config.players[self.current_player].key_binding.action)
        self.up_button.text = 'Up key: ' + pygame.key.name(
            config.players[self.current_player].key_binding.upward)
        self.down_button.text = 'Down key: ' + pygame.key.name(
            config.players[self.current_player].key_binding.down)
        self.left_button.text = 'Left key: ' + pygame.key.name(
            config.players[self.current_player].key_binding.left)
        self.right_button.text = 'Right key: ' + pygame.key.name(
            config.players[self.current_player].key_binding.right)

    def set_key(self, key):
        """ sets new key for key mapping for current player """
        if self.selected == 1:
            config.players[self.current_player].key_binding.action = key
        elif self.selected == 2:
            config.players[self.current_player].key_binding.upward = key
        elif self.selected == 3:
            config.players[self.current_player].key_binding.down = key
        elif self.selected == 4:
            config.players[self.current_player].key_binding.left = key
        else:
            config.players[self.current_player].key_binding.right = key
        self.update_keys()

    def on_click(self, button: Button):
        """Button functions"""
        if button is self.player_button:
            self.change_current_player()
            self.update_keys()
        elif button is self.action_button:
            self.update_keys()
            pass
            # config.players[self.current_player].key_binding.action = key
        elif button is self.up_button:
            self.update_keys()
            pass
            # config.players[self.current_player].key_binding.upward = key
        elif button is self.down_button:
            self.update_keys()
            pass
            # config.players[self.current_player].key_binding.down = key
        elif button is self.left_button:
            self.update_keys()
            pass
            # config.players[self.current_player].key_binding.left = key
        elif button is self.right_button:
            self.update_keys()
            pass
            # config.players[self.current_player].key_binding.right = key
        elif button is self.exit_button:
            state_manager.pop()

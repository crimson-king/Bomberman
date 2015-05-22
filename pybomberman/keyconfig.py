"""
This module implements functionality that allows user to view and change key
 mappings.
"""
__author__ = 'Tomasz Rzepka'
import pygame

from framework.state import State
from pybomberman.menu import Item
from pybomberman.config import config
from framework import state_manager


BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)
pygame.init()


class KeyConfigState(State):
    """
    This class implements State that allows user to view and change key
    mappings
    """
    def __init__(self, width, height):
        self.width = width / 2
        self.height = height / 2
        self.current_player = 0
        self.selecting_key = False
        option_functions = (('Player <%d> keys' % (self.current_player + 1),
                             self.change_current_player),
                            ('Action: ' +
                             pygame.key.name(
                                 config.player_key_configs[self.current_player]
                                     .action), self.select_key),
                            ('Up key: ' +
                             pygame.key.name(
                                 config.player_key_configs[self.current_player]
                                     .up), self.select_key),
                            ('Down key: ' +
                             pygame.key.name(
                                 config.player_key_configs[self.current_player]
                                     .down), self.select_key),
                            ('Left key: ' +
                             pygame.key.name(
                                 config.player_key_configs[self.current_player]
                                     .left), self.select_key),
                            ('Right key: ' +
                             pygame.key.name(
                                 config.player_key_configs[self.current_player]
                                     .right), self.select_key),
                            ('Go Back', state_manager.pop))
        self.items = []
        for i, item in enumerate(option_functions):
            self.items.append(Item(item, size=35))
        self.selected = 0

        for i, menu_item in enumerate(self.items):
            height = menu_item.height * len(self.items)
            if i == 0 or i == len(self.items) - 1:
                x_coordinate = self.width - menu_item.width / 2
            else:
                x_coordinate = self.width - 200
            y_coordinate = self.height / 2 - height / 2 + i * 2 + 2 * i * menu_item.height
            menu_item.set_position(x_coordinate, y_coordinate)

    def select_key(self):
        """ Prepares key for new mapping """
        self.items[self.selected].text = \
            self.items[self.selected].text.rsplit(':', 1)[0]
        self.items[self.selected].text += ": <select key>"
        self.selecting_key = True

    def change_current_player(self):
        """ selects next available for which settings are being set """
        self.current_player = (
            (self.current_player + 1) % config.players)
        self.items[self.selected].text = "Player <%d> keys" % (
            self.current_player + 1)
        self.update_keys()

    def update_keys(self):
        """ updates key names for key mappings for current player """
        self.items[1].text = 'Action: ' + pygame.key.name(
            config.player_key_configs[self.current_player].action)
        self.items[2].text = 'Up key: ' + pygame.key.name(
            config.player_key_configs[self.current_player].up)
        self.items[3].text = 'Down key: ' + pygame.key.name(
            config.player_key_configs[self.current_player].down)
        self.items[4].text = 'Left key: ' + pygame.key.name(
            config.player_key_configs[self.current_player].left)
        self.items[5].text = 'Right key: ' + pygame.key.name(
            config.player_key_configs[self.current_player].right)

    def set_key(self, key):
        """ sets new key for key mapping for current player """
        if self.selected == 1:
            config.player_key_configs[self.current_player].action = key
        elif self.selected == 2:
            config.player_key_configs[self.current_player].up = key
        elif self.selected == 3:
            config.player_key_configs[self.current_player].down = key
        elif self.selected == 4:
            config.player_key_configs[self.current_player].left = key
        else:
            config.player_key_configs[self.current_player].right = key
        self.update_keys()

    def handle_draw(self, canvas):
        """ draws current state """
        canvas.fill((40, 60, 190))
        for item in self.items:
            canvas.blit(item.label, item.position)
            item.highlight(BLACK)
        self.items[self.selected].highlight(CRIMSON)

    def handle_input(self, event):
        """ handles input from user """
        if event.type == pygame.KEYDOWN:
            if self.selecting_key:
                self.set_key(event.key)
                self.selecting_key = False
            elif event.key == pygame.K_DOWN:
                if self.selected < len(self.items) - 1:
                    self.selected += 1
                else:
                    self.selected = 0
            elif event.key == pygame.K_UP:
                if self.selected == 0:
                    self.selected = len(self.items) - 1
                else:
                    self.selected -= 1
            elif event.key == pygame.K_RETURN:  # K_RETURN = enter
                self.items[self.selected].function()

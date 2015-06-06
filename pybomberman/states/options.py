"""Options"""
import pygame
from framework.ui import StageState, Text, Button
from framework import state_manager
from pybomberman.config import config
from pybomberman.states.keyconfig import KeyConfigState

# pylint: disable=no-member
BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)
pygame.init()


class OptionsState(StageState):
    """This is a state for options."""
    def __init__(self):
        super().__init__()
        title_view = Text('PyBomberman')
        self.stage.add_node(title_view)

        self.player_button = Button('AMOUNT OF PLAYERS: <%d>' % config.player_count,
                                    focused_color=CRIMSON)
        self.player_button.on_click = self.on_click
        self.stage.add_node(self.player_button)

        self.resolution_button = Button('RESOLUTION',
                                        focused_color=CRIMSON)
        self.stage.add_node(self.resolution_button)
        self.resolution_button.on_click = self.on_click

        self.key_config_button = Button('PLAYER KEY CONFIGURATION',
                                        focused_color=CRIMSON)
        self.stage.add_node(self.key_config_button)
        self.key_config_button.on_click = self.on_click

        self.exit_button = Button('GO BACK', focused_color=CRIMSON)
        self.stage.add_node(self.exit_button)
        self.exit_button.on_click = self.on_click

    def on_click(self, button: Button):
        """Button functions"""
        if button is self.player_button:
            self.chooseplayers()
        elif button is self.resolution_button:
            print('NotYetImplemented')
        elif button is self.key_config_button:
            state_manager.push(KeyConfigState())
        elif button is self.exit_button:
            config.save()
            state_manager.pop()

    def chooseplayers(self):
        """Switches amount of players"""
        config.player_count += 1
        if config.player_count > len(config.players):
            config.player_count = 2
        self.player_button.text = "AMOUNT OF PLAYERS: <%d>" % config.player_count

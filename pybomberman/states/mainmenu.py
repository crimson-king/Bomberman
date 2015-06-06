"""Main menu"""

from framework.ui import StageState, Text, Button
from framework import state_manager

from pybomberman.states.game import GameState
from pybomberman.states.options import OptionsState

CRIMSON = (220, 20, 60)

class MainMenuState(StageState):
    """Main Menu State"""
    def __init__(self):
        super().__init__()
        title_view = Text('PyBomberman')
        self.stage.add_node(title_view)

        self.play_button = Button('PLAY', focused_color=CRIMSON)
        self.play_button.on_click = self.on_click
        self.stage.add_node(self.play_button)

        self.settings_button = Button('SETTINGS', focused_color=CRIMSON)
        self.stage.add_node(self.settings_button)
        self.settings_button.on_click = self.on_click

        self.exit_button = Button('EXIT', focused_color=CRIMSON)
        self.stage.add_node(self.exit_button)
        self.exit_button.on_click = self.on_click

    def on_click(self, button: Button):
        """Button functions"""
        if button is self.play_button:
            state_manager.push(GameState())
        elif button is self.settings_button:
            state_manager.push(OptionsState())
        elif button is self.exit_button:
            state_manager.pop()

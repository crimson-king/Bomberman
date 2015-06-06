"""A facade, used for running the game"""
import sys

from framework.core import Game
from framework.state import StateGameHandler
from framework import state_manager
from pybomberman.keyconfig import KeyConfigState
from pybomberman.menu import MenuState, Item
from pybomberman.options import OptionsState
from pybomberman.config import config
from pybomberman.gamestate import GameState


class Facade:
    """What the string above said."""
    def __init__(self):
        self.items = []

    def startgame(self):
        """Starts the game"""
        state_manager.push(GameState())
        Game(handler=StateGameHandler()).start()

    def run_game(self):
        """Runs the game"""
        def backtomenu():
            """Goes back to menu and saves settings"""
            config.save()
            state_manager.pop()

        def chooseplayers(item: Item):
            """Switches amount of players"""
            config.player_count += 1
            if config.player_count > len(config.players):
                config.player_count = 2
            item.text = "Amount of players: <%d>" % config.player_count

        def options():
            """Goes to options state"""
            optionfunctions = (('Amount of players: <%d>' % config.player_count, chooseplayers),
                               ('Resolution', backtomenu),
                               ('Key bindings', key_bindings), ('Go back', backtomenu))
            self.items = []
            for item in optionfunctions:
                self.items.append(Item(item))
            state_manager.push(OptionsState(*config.resolution, items=self.items))
            Game(handler=StateGameHandler()).start()

        def key_bindings():
            """Goes to key config state"""
            state_manager.push(KeyConfigState(*config.resolution))
            Game(handler=StateGameHandler()).start()

        texts = (('Start', self.startgame), ('Options', options), ('Exit', sys.exit))
        state_manager.push(MenuState(*config.resolution, texts=texts))
        Game(StateGameHandler(), 60, *config.resolution).start()

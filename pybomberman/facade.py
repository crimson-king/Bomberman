import sys

from framework.core import Game
from framework.state import StateGameHandler
from framework import state_manager
from pybomberman.menu import MenuState, Item
from pybomberman.options import OptionsState
from pybomberman.configuration import configuration


class Facade:

    def run_game(self):

        scr_width = 960
        scr_height = 600

        def backtomenu():
            state_manager.pop()

        def chooseplayers(item: Item):
            if configuration.players == 2:
                configuration.players = 3
                item.text = "Amount of players: <3>"
            elif configuration.players == 3:
                configuration.players = 4
                item.text = "Amount of players: <4>"
            else:
                configuration.players = 2
                item.text = "Amount of players: <2>"

        def options():
            optionfunctions = (('Amount of players: <2>', chooseplayers), ('Resolution', 'tmp'),
                               ('Key bindings', 'tmp'), ('Go back', backtomenu))
            items = []
            for i, item in enumerate(optionfunctions):
                items.append(Item(item))
            state_manager.push(OptionsState(scr_width, scr_height, items))
            Game(handler=StateGameHandler()).start()

        texts = (('Start', 'start_game'), ('Options', options), ('Exit', sys.exit))

        state_manager.push(MenuState(scr_width, scr_height, texts))
        Game(handler=StateGameHandler()).start()

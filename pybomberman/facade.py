import sys

from framework.core import Game
from framework.state import StateGameHandler
from framework import state_manager
from pybomberman.menu import MenuState
from pybomberman.options import OptionsState


class Facade:

    def run_game(self):

        scr_width = 960
        scr_height = 600

        def backtomenu():
            state_manager.pop()

        def options():
            optionfunctions = (('Amount of players', 'tmp'), ('Resolution', 'tmp'),
                               ('Key bindings', 'tmp'), ('Go back', backtomenu))
            state_manager.push(OptionsState(scr_width, scr_height, optionfunctions))
            Game(handler=StateGameHandler()).start()

        texts = (('Start', 'start_game'), ('Options', options), ('Exit', sys.exit))

        state_manager.push(MenuState(scr_width, scr_height, texts))
        Game(handler=StateGameHandler()).start()

import sys

from framework.core import Game
from framework.state import StateGameHandler
from framework import state_manager
from pybomberman.menu import MenuState


class Facade:
    def run_game(self):
        texts = (('Start', 'start_game'), ('Options', 'options'), ('Exit', sys.exit))
        scr_width = 960
        scr_height = 600
        state_manager.push(MenuState(scr_width, scr_height, texts))
        Game(handler=StateGameHandler()).start()

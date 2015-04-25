from pybomberman.core import *
from pybomberman.state import *
from pybomberman.menu import *
import sys


class Facade:

    def run_game(self):
        texts = (('Start', 'start_game'), ('Options', 'options'), ('Exit', sys.exit))
        scr_width = 960
        scr_height = 600
        manager.push(MenuState(scr_width, scr_height, texts))
        Game(handler=StateGameHandler()).start()

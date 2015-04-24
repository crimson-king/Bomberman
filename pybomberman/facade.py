from pybomberman.core import *
from pybomberman.state import *
from pybomberman.menu import *


class Facade:

    def run_game():
        texts = ('Start', 'Options', 'Exit')
        scr_width = 960
        scr_height = 600
        manager.push(MenuState(scr_width, scr_height, texts))
        Game(handler=StateGameHandler()).start()

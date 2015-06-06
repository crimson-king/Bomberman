"""Init module containing methods to run pybomberman with ease."""

import os


PPM = 64

ASSETS_PATH = os.path.join(os.path.curdir, 'assets')
print('assets dir:', os.path.realpath(ASSETS_PATH))


def main():
    """Starts pybomberman."""
    from framework.core import Game
    from framework.state import StateGameHandler
    from framework import state_manager
    from pybomberman.states.game import GameState
    from pybomberman.config import config
    from pybomberman.states.mainmenu import MainMenuState

    game = Game(StateGameHandler(), 60, *config.resolution)
    state_manager.push(MainMenuState())
    game.start()

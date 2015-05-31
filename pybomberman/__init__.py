"""Init module containing methods to run pybomberman with ease."""

PPM = 50


def main():
    """Starts pybomberman."""
    from framework.core import Game
    from framework.state import StateGameHandler
    from framework import state_manager
    from pybomberman.gamestate import GameState
    from pybomberman.config import config

    state_manager.push(GameState())
    Game(StateGameHandler(), 60, *config.resolution).start()

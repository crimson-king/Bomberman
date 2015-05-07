import sys

from framework.core import Game
from framework.state import StateGameHandler
from framework import state_manager
from pybomberman.keyconfig import KeyConfigState
from pybomberman.menu import MenuState, Item
from pybomberman.options import OptionsState
from pybomberman.configuration import configuration
from pybomberman.gamestate import GameState


class Facade:

    def run_game(self):

        scr_width = 960
        scr_height = 600

        def backtomenu():
            state_manager.pop()

        def chooseplayers(item: Item):
            configuration.players += 1
            if configuration.players > configuration.max_players:
                configuration.players = 2
            item.text = "Amount of players: <%d>" % configuration.players

        def startgame():
            state_manager.push(GameState())
            Game(handler=StateGameHandler()).start()

        def options():
            optionfunctions = (('Amount of players: <2>', chooseplayers), ('Resolution', 'tmp'),
                               ('Key bindings', key_bindings), ('Go back', backtomenu))
            items = []
            for i, item in enumerate(optionfunctions):
                items.append(Item(item))
            state_manager.push(OptionsState(scr_width, scr_height, items))
            Game(handler=StateGameHandler()).start()

        def key_bindings():
            state_manager.push(KeyConfigState(scr_width, scr_height))
            Game(handler=StateGameHandler()).start()


        texts = (('Start', startgame), ('Options', options), ('Exit', sys.exit))

        state_manager.push(MenuState(scr_width, scr_height, texts))
        Game(handler=StateGameHandler()).start()

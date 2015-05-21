import sys
import pygame
import json

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
            settings = {'players': {'amount': configuration.players},
                        'p1keys': {'left': configuration.player_key_configs[1].left,
                                   'right': configuration.player_key_configs[1].right,
                                   'up': configuration.player_key_configs[1].up,
                                   'down': configuration.player_key_configs[1].down,
                                   'action': configuration.player_key_configs[1].action},
                        'p2keys': {'left': configuration.player_key_configs[2].left,
                                   'right': configuration.player_key_configs[2].right,
                                   'up': configuration.player_key_configs[2].up,
                                   'down': configuration.player_key_configs[2].down,
                                   'action': configuration.player_key_configs[2].action},
                        'p3keys': {'left': configuration.player_key_configs[3].left,
                                   'right': configuration.player_key_configs[3].right,
                                   'up': configuration.player_key_configs[3].up,
                                   'down': configuration.player_key_configs[3].down,
                                   'action': configuration.player_key_configs[3].action},
                        'p0keys': {'left': configuration.player_key_configs[0].left,
                                   'right': configuration.player_key_configs[0].right,
                                   'up': configuration.player_key_configs[0].up,
                                   'down': configuration.player_key_configs[0].down,
                                   'action': configuration.player_key_configs[0].action}}
            with open('settings.json', 'w') as outfile:
                json.dump(settings, outfile)
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
            optionfunctions = (('Amount of players: <%d>' % configuration.players, chooseplayers),
                               ('Resolution', backtomenu), ('Key bindings', key_bindings), ('Go back', backtomenu))
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

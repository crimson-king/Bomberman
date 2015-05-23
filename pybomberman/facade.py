import sys
import json

from framework.core import Game
from framework.state import StateGameHandler
from framework import state_manager
from pybomberman.keyconfig import KeyConfigState
from pybomberman.menu import MenuState, Item
from pybomberman.options import OptionsState
from pybomberman.config import config
from pybomberman.gamestate import GameState


class Facade:

    def run_game(self):

        def backtomenu():
            settings = {'players': {'amount': config.players},
                        'p1keys': {'left': config.player_key_configs[1].left,
                                   'right': config.player_key_configs[1].right,
                                   'up': config.player_key_configs[1].up,
                                   'down': config.player_key_configs[1].down,
                                   'action': config.player_key_configs[1].action},
                        'p2keys': {'left': config.player_key_configs[2].left,
                                   'right': config.player_key_configs[2].right,
                                   'up': config.player_key_configs[2].up,
                                   'down': config.player_key_configs[2].down,
                                   'action': config.player_key_configs[2].action},
                        'p3keys': {'left': config.player_key_configs[3].left,
                                   'right': config.player_key_configs[3].right,
                                   'up': config.player_key_configs[3].up,
                                   'down': config.player_key_configs[3].down,
                                   'action': config.player_key_configs[3].action},
                        'p0keys': {'left': config.player_key_configs[0].left,
                                   'right': config.player_key_configs[0].right,
                                   'up': config.player_key_configs[0].up,
                                   'down': config.player_key_configs[0].down,
                                   'action': config.player_key_configs[0].action}}
            with open('settings.json', 'w') as outfile:
                json.dump(settings, outfile)
            state_manager.pop()

        def chooseplayers(item: Item):
            config.player_count += 1
            if config.player_count > len(config.players):
                config.player_count = 2
            item.text = "Amount of players: <%d>" % config.player_count

        def startgame():
            state_manager.push(GameState())
            Game(handler=StateGameHandler()).start()

        def options():
            optionfunctions = (('Amount of players: <%d>' % config.player_count, chooseplayers),
                               ('Resolution', backtomenu), ('Key bindings', key_bindings), ('Go back', backtomenu))
            items = []
            for i, item in enumerate(optionfunctions):
                items.append(Item(item))
            state_manager.push(OptionsState(*config.resolution, items=items))
            Game(handler=StateGameHandler()).start()

        def key_bindings():
            state_manager.push(KeyConfigState(*config.resolution))
            Game(handler=StateGameHandler()).start()

        texts = (('Start', startgame), ('Options', options), ('Exit', sys.exit))
        state_manager.push(MenuState(*config.resolution, texts=texts))
        Game(StateGameHandler(), 60, *config.resolution).start()

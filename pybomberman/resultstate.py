"""You will find Result State here"""

from framework.ui import StageState, Text, Button
from framework import state_manager


class ResultState(StageState):
    """State displaying final game results"""

    def __init__(self, players):
        super().__init__()
        for i, player in enumerate(players):
            result = 'wins' if player.health > 0 else 'loses'
            text_view = Text('Player {} {result}, kills: {kills}'
                             .format(i, result=result, **player.__dict__))
            self.stage.add_node(text_view)

        self.again_button = Button('Again')
        self.stage.add_node(self.again_button)

        self.menu_button = Button('Menu')
        self.menu_button.on_click = self.on_click
        self.stage.add_node(self.menu_button)

    def on_click(self, button: Button):
        """Handles buttons clicks"""
        if button is self.menu_button:
            state_manager.pop()
        elif button is self.again_button:
            state_manager.pop()
            from pybomberman.gamestate import GameState

            state_manager.push(GameState())

    def destroy(self):
        """Does nothing. Except shutting pylint's too-few-public-methods up"""
        pass

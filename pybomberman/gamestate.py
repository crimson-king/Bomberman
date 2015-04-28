from framework.state import State


class GameState(State):
    def handle_draw(self, canvas):
        canvas.fill((20, 20, 200))

    def handle_input(self, event):
        pass

    def handle_update(self, dt):
        pass
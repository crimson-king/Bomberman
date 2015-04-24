from state import State


class OptionsState(State):
    def handle_draw(self, canvas):
        canvas.fill((20, 200, 20))

    def handle_input(self, event):
        pass

    def handle_update(self, dt):
        pass
from framework.core import GameHandler, Game


class State(GameHandler):
    def start(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def destroy(self):
        pass


class StateManager(GameHandler):
    def __init__(self):
        self._states = []

    def push(self, state: State):
        print('pushing state', state)
        if self._states:
            self._states[-1].pause()

        state.start()
        self._states.append(state)
        state.resume()

    def pop(self) -> State:
        state = self._states[-1]
        print('popping state', state)
        state.pause()
        self._states.pop()
        state.destroy()

        if self._states:
            self._states[-1].resume()

        return state

    def handle_input(self, event):
        if self._states:
            self._states[-1].handle_input(event)

    def handle_update(self, dt):
        if self._states:
            self._states[-1].handle_update(dt)

    def handle_draw(self, canvas):
        if self._states:
            self._states[-1].handle_draw(canvas)

    def running(self):
        return bool(self._states)


manager = StateManager()


class StateGameHandler(GameHandler):
    def handle_input(self, event):
        manager.handle_input(event)

    def handle_update(self, dt):
        manager.handle_update(dt)

    def handle_draw(self, canvas):
        manager.handle_draw(canvas)

    def running(self):
        return manager.running()


if __name__ == '__main__':
    class SampleGameHandler(StateGameHandler):

        max_state_time = 2000

        def __init__(self):
            manager.push(SampleGameHandler.RedState())

        class TimedColorState(State):
            def __init__(self, color):
                self.time = 0
                self.color = color

            def handle_update(self, dt):
                self.time += dt
                if self.time >= SampleGameHandler.max_state_time:
                    self.state_end()

            def handle_draw(self, canvas):
                canvas.fill(self.color)

            def state_end(self):
                raise NotImplementedError

        class YellowState(TimedColorState):
            def __init__(self):
                super().__init__(color=(0xff, 0xff, 0))

            def state_end(self):
                manager.pop()

        class RedState(TimedColorState):
            def __init__(self):
                super().__init__(color=(0xff, 0, 0))

            def resume(self):
                self.time = 0

            def state_end(self):
                manager.push(SampleGameHandler.YellowState())

    print('running state demo..')
    Game(handler=SampleGameHandler()).start()

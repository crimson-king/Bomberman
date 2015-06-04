"""
This submodule has State interface derived from GameHandler,
which subclass instances are operated by StateManager. To use this feature,
you need to pass StateGameHandler to Game's initializer.
"""

from framework.core import GameHandler, Game


class State(GameHandler):
    """State 'interface'. Intended to use with StateManager"""

    def start(self):
        """Called when this state is about to be displayed for the first
        time"""
        pass

    def pause(self):
        """Called when this state is about to be covered by another state"""
        pass

    def resume(self):
        """Called when this state is about to be uncovered"""
        pass

    def destroy(self):
        """Called when this state will not be used again in state manager
        stack. If you'll push it again anyways, start method will be called"""
        pass


class StateManager(GameHandler):
    """Manages state. To display new state, use push(). To dispose active
    state, use pop(). Implement State methods appropriately"""

    def __init__(self):
        self._states = []

    def push(self, state: State):
        """Pushes state intended to be shown to stack. pause() method shall
        be called on active state if any. start() and then resume() methods
        will be called on given state"""
        print('pushing state', state)
        if self._states:
            self._states[-1].pause()

        state.start()
        self._states.append(state)
        state.resume()

    def pop(self) -> State:
        """Pops active state from stack. pause() and destroy() methods are
        called on active state. If stack is empty, running() method will
        return False and application should quit"""
        state = self._states[-1]
        print('popping state', state)
        state.pause()
        self._states.pop()
        state.destroy()

        if self._states:
            self._states[-1].resume()

        return state

    def handle_input(self, event):
        """Forwards event to active state"""
        if self._states:
            self._states[-1].handle_input(event)

    def handle_update(self, delta_time):
        """Forwards event to active state"""
        if self._states:
            self._states[-1].handle_update(delta_time)

    def handle_draw(self, canvas):
        """Forwards event to active state"""
        if self._states:
            self._states[-1].handle_draw(canvas)

    def running(self) -> bool:
        """True if stack isn't empty, False otherwise"""
        return bool(self._states)

# it is not a constant
# pylint: disable=invalid-name
manager = StateManager()


class StateGameHandler(GameHandler):
    """Use this class as Game's handler if you want to use State interface"""

    def handle_input(self, event):
        """Forwards event to state manager"""
        manager.handle_input(event)

    def handle_update(self, delta_time):
        """Forwards event to state manager"""
        manager.handle_update(delta_time)

    def handle_draw(self, canvas):
        """Forwards event to state manager"""
        manager.handle_draw(canvas)

    def running(self):
        """Forwards event to state manager"""
        return manager.running()


if __name__ == '__main__':
    MAX_STATE_TIME = 2000

    class TimedColorState(State):
        """Example"""

        def __init__(self, color):
            self.time = 0
            self.color = color

        def handle_update(self, dt):
            """Example"""
            self.time += dt
            if self.time >= MAX_STATE_TIME:
                self.state_end()

        def handle_draw(self, canvas):
            """Example"""
            canvas.fill(self.color)

        def state_end(self):
            """Example"""
            raise NotImplementedError

    class YellowState(TimedColorState):
        """Example"""

        def __init__(self):
            super().__init__(color=(0xff, 0xff, 0))

        def state_end(self):
            """Example"""
            manager.pop()

        def resume(self):
            pass

    class RedState(TimedColorState):
        """Example"""

        def __init__(self):
            super().__init__(color=(0xff, 0, 0))

        def resume(self):
            """Example"""
            self.time = 0

        def state_end(self):
            """Example"""
            manager.push(YellowState())

    print('running state demo..')
    manager.push(RedState())
    Game(handler=StateGameHandler()).start()

from enum import Enum, unique

import pygame


class Action:
    def __bool__(self):
        return self.active()

    def active(self):
        raise NotImplementedError

    def press(self):
        pass

    def release(self):
        pass

    def reset(self):
        pass


class NormalAction(Action):
    @unique
    class State(Enum):
        released = 0
        pressed = 1

    def __init__(self):
        self.state = NormalAction.State.released

    def active(self):
        return self.state is NormalAction.State.pressed

    def press(self):
        self.state = NormalAction.State.pressed

    def release(self):
        self.state = NormalAction.State.released

    def reset(self):
        self.state = NormalAction.State.released


class InitialAction(Action):
    @unique
    class State(Enum):
        inactive = 0
        active = 1

    def __init__(self):
        self.state = InitialAction.State.inactive

    def active(self):
        if self.state is InitialAction.State.active:
            self.state = InitialAction.State.inactive
            return True
        return False

    def press(self):
        self.state = InitialAction.State.active

    def reset(self):
        self.state = InitialAction.State.inactive


class InputManager:
    def __init__(self):
        self._action_map = {}

    def map_action(self, key_code, action: Action):
        self._action_map[key_code] = action

    def handle_input(self, event):
        if not hasattr(event, 'key'):
            return

        action = self._action_map.get(event.key, None)

        if action is None:
            return

        if event.type == pygame.KEYDOWN:
            action.press()
        elif event.type == pygame.KEYUP:
            action.release()

    def reset(self):
        for action in self._action_map.values():
            action.reset()

    def clear(self):
        self._action_map.clear()


manager = InputManager()

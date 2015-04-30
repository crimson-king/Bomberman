from enum import Enum, unique


class InputManager:
    actions = {}


class Action:
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

    def __bool__(self):
        return bool(self)


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

    def press(self):
        self.state = InitialAction.State.active

    def reset(self):
        self.state = InitialAction.State.inactive

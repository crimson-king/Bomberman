"""
Contains classes related to processing input events like Action or
InputManager.
Allows easy use of PyGame key input (although it can be easily
adapted to handle other input as well). Action interface along with
straightforward NormalAction and almost as trivial InitialAction managed by
InputManager may be used as deadly simple, yet powerful and extensible input
processor.
"""

from enum import Enum, unique

# pygame modules are loaded dynamically, thus, supress no name/members errors
# pylint: disable=no-name-in-module
# pylint: disable=no-member
import pygame


class Action:
    """Pseudo-abstract class for action"""

    def __bool__(self):
        return self.active()

    def active(self) -> bool:
        """Is it active?"""
        raise NotImplementedError

    def press(self):
        """Invoked on key down event"""
        pass

    def release(self):
        """Invoked on key up event"""
        pass

    def reset(self):
        """Resets action to initial state"""
        pass


class NormalAction(Action):
    """Action that is active as long as key is pressed"""

    @unique
    class State(Enum):
        """Internal state enum"""
        released = 0
        pressed = 1

    def __init__(self):
        self.state = NormalAction.State.released

    def active(self) -> bool:
        """True if its active, False otherwise"""
        return self.state is NormalAction.State.pressed

    def press(self):
        """Invoked on key down event"""
        self.state = NormalAction.State.pressed

    def release(self):
        """Invoked on key up event"""
        self.state = NormalAction.State.released

    def reset(self):
        """Resets action to initial state"""
        self.state = NormalAction.State.released


class InitialAction(Action):
    """Action active only once per press"""

    @unique
    class State(Enum):
        """Internal state enum"""
        inactive = 0
        active = 1

    def __init__(self):
        self.state = InitialAction.State.inactive

    def active(self) -> bool:
        """True if its active, False otherwise"""
        if self.state is InitialAction.State.active:
            self.state = InitialAction.State.inactive
            return True
        return False

    def press(self):
        """Invoked on key down event"""
        self.state = InitialAction.State.active

    def reset(self):
        """Resets action to initial state"""
        self.state = InitialAction.State.inactive


class InputManager:
    """Manages Actions mapped with map_action to given key codes"""

    def __init__(self):
        self._action_map = {}

    def map_action(self, key_code, action: Action):
        """Maps given action to given key code"""
        self._action_map[key_code] = action

    def handle_input(self, event):
        """Invokes mapped actions press() and release() methods"""

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
        """Resets all mapped actions"""
        for action in self._action_map.values():
            action.reset()

    def clear(self):
        """Clears action map"""
        self._action_map.clear()


# this is not a constant
# pylint: disable=invalid-name
manager = InputManager()

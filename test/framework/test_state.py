"""State tests"""
from unittest import TestCase
from framework import state_manager as manager
from framework.state import State

STATE_TIME = 2000


class ColorState(State):
    """Example"""

    def __init__(self, color):
        self.time = 0
        self.color = color

    def handle_update(self, dt):
        """Example"""
        self.time += dt
        if self.time >= STATE_TIME:
            self.state_end()

    def handle_draw(self, canvas):
        """Example"""
        canvas.fill(self.color)

    def state_end(self):
        """Example"""
        raise NotImplementedError


class BlackState(ColorState):
    """Example"""

    def __init__(self):
        super().__init__(color=(0xff, 0xff, 0))

    def state_end(self):
        """Example"""
        manager.pop()

    def resume(self):
        pass


class GreenState(ColorState):
    """Example"""

    def __init__(self):
        super().__init__(color=(0xff, 0, 0))

    def resume(self):
        """Example"""
        self.time = 0

    def state_end(self):
        """Example"""
        manager.push(GreenState())


class TestState(TestCase):
    """Tests for State/State Manager"""
    def testManager(self):
        """Tests adding states to the state manager"""
        self.assertFalse(manager.running())
        manager.push(GreenState())
        self.assertTrue(manager.running())
        manager.pop()
        self.assertFalse(manager.running())
        manager.push(BlackState())
        self.assertTrue(manager.running())
        manager.push(GreenState())
        self.assertTrue(manager.running())
        manager.pop()
        self.assertTrue(manager.running())


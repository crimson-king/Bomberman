from unittest import TestCase

from framework.input import NormalAction, InitialAction


class TestNormalAction(TestCase):
    def test(self):
        action = NormalAction()

        self.assertFalse(action.active())
        self.assertFalse(action.active())

        action.press()

        self.assertTrue(action.active())
        self.assertTrue(action.active())

        action.release()

        self.assertFalse(action.active())
        self.assertFalse(action.active())


class TestInitialAction(TestCase):
    def test_mode_initial_only(self):
        action = InitialAction()

        self.assertFalse(action.active())
        self.assertFalse(action.active())

        action.press()

        self.assertTrue(action.active())
        self.assertFalse(action.active())

        action.release()

        self.assertFalse(action.active())
        self.assertFalse(action.active())

        action.press()
        action.press()
        action.release()
        action.release()

        self.assertTrue(action.active())
        self.assertFalse(action.active())
"""Physics tests"""
from unittest import TestCase
from pybomberman.shapes import Rectangle
from pybomberman.physics import collides_rect


class TestPhysics(TestCase):
    """Tests physics"""
    def test_rect_collision(self):
        """Tests rectangle collision"""
        recta = Rectangle(0, 0, 20, 20)
        ngle = Rectangle(0, 0, 5, 10)
        remote_rect = Rectangle(1000, 1000, 10, 10)
        square = Rectangle(15, 15, 5, 5)

        self.assertTrue(collides_rect(recta, ngle))
        self.assertFalse(collides_rect(recta, remote_rect))
        self.assertFalse(collides_rect(remote_rect, ngle))
        self.assertTrue(collides_rect(recta, square))
        self.assertFalse(collides_rect(square, remote_rect))
        self.assertFalse(collides_rect(ngle, square))

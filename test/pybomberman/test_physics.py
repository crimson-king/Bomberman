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
        square = Rectangle(15, 15, 10, 10)
        recta_touch = Rectangle(20, 20, 40, 40)
        mother_rect = Rectangle(-10, -10, 20000, 20000)

        self.assertTrue(collides_rect(recta, ngle))
        self.assertFalse(collides_rect(recta, remote_rect))
        self.assertFalse(collides_rect(remote_rect, ngle))
        self.assertTrue(collides_rect(recta, square))
        self.assertFalse(collides_rect(square, remote_rect))
        self.assertFalse(collides_rect(ngle, square))

        self.assertFalse(collides_rect(recta_touch, recta))
        self.assertFalse(collides_rect(recta_touch, ngle))
        self.assertFalse(collides_rect(recta_touch, remote_rect))
        self.assertTrue(collides_rect(recta_touch, square))

        self.assertTrue(collides_rect(mother_rect, recta))
        self.assertTrue(collides_rect(mother_rect, ngle))
        self.assertTrue(collides_rect(mother_rect, remote_rect))
        self.assertTrue(collides_rect(mother_rect, square))
        self.assertTrue(collides_rect(mother_rect, recta_touch))

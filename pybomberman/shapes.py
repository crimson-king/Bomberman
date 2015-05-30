"""Shape classes are here"""
from itertools import chain
from numbers import Real

from pygame.math import Vector2


class Shape:
    """Abstract shape class"""
    def move(self, x=0, y=0):
        """Abstract move method"""
        raise NotImplementedError


class Rectangle(Shape):
    """Any quadrilateral with four right angles"""
    def __init__(self, x=0, y=0, width=0, height=0):
        self.position = Vector2()
        self.position.x = x
        self.position.y = y
        self.size = Vector2()
        self.size.x = width
        self.size.y = height

    @property
    def x(self):
        """Returns x"""
        return self.position.x

    @x.setter
    def x(self, value):
        """Sets x"""
        self.position.x = value

    @property
    def y(self):
        """Returns y"""
        return self.position.y

    @y.setter
    def y(self, value):
        """Sets y"""
        self.position.y = value

    @property
    def width(self):
        """Returns width"""
        return self.size.x

    @width.setter
    def width(self, value):
        """Sets width"""
        self.size.x = value

    @property
    def height(self):
        """Returns height"""
        return self.size.y

    @height.setter
    def height(self, value):
        """Sets height"""
        self.size.y = value

    @property
    def center(self):
        """Returns center of the rectangle"""
        return self.position + self.size * .5

    @center.setter
    def center(self, x: Real, y: Real):
        """Sets the center"""
        self.position.set(x - .5 * self.width, y - .5 * self.height)

    def move(self, x: Real=0, y: Real=0):
        """Moves the object"""
        self.position += (x, y)

    def __repr__(self):
        """Returns weird representation of the object"""
        return '<{}: ({}, {}, {}, {})>'.format(
            self.__class__.__name__, *chain(self.position, self.size))

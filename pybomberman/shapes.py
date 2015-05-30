"""Shape classes are here"""
from itertools import chain
from numbers import Real

from pygame.math import Vector2


class Shape:
    def __init__(self):
        pass

    """Abstract shape class"""
    def move(self, pos_x=0, pos_y=0):
        """Abstract move method"""
        raise NotImplementedError


class Rectangle(Shape):
    """Any quadrilateral with four right angles"""
    def __init__(self, pos_x=0, pos_y=0, width=0, height=0):
        self.position = Vector2()
        self.position.x = pos_x
        self.position.y = pos_y
        self.size = Vector2()
        self.size.x = width
        self.size.y = height

    @property
    def pos_x(self):
        """Returns x"""
        return self.position.x

    @pos_x.setter
    def pos_x(self, value):
        """Sets x"""
        self.position.x = value

    @property
    def pos_y(self):
        """Returns y"""
        return self.position.y

    @pos_y.setter
    def pos_y(self, value):
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
    def center(self, pos_x: Real, pos_y: Real):
        """Sets the center"""
        self.position.set(pos_x - .5 * self.width, pos_y - .5 * self.height)

    def move(self, pos_x: Real=0, pos_y: Real=0):
        """Moves the object"""
        self.position += (pos_x, pos_y)

    def __repr__(self):
        """Returns weird representation of the object"""
        return '<{}: ({}, {}, {}, {})>'.format(
            self.__class__.__name__, *chain(self.position, self.size))

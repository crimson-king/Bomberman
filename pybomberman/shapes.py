from numbers import Real

from pygame.math import Vector2


class Shape:
    def move(self, x=0, y=0):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, x=0, y=0, width=0, height=0):
        self.position = Vector2()
        self.position.x = x
        self.position.y = y
        self.size = Vector2()
        self.size.x = width
        self.size.y = height

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.x = value

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.y = value

    @property
    def width(self):
        return self.size.x

    @width.setter
    def width(self, value):
        self.size.x = value

    @property
    def height(self):
        return self.size.y

    @height.setter
    def height(self, value):
        self.size.y = value

    @property
    def center(self):
        return self.position + self.size * .5

    @center.setter
    def center(self, x: Real, y: Real):
        self.position.set(x - .5 * self.width, y - .5 * self.height)

    def move(self, x: Real=0, y: Real=0):
        self.position.move(x, y)

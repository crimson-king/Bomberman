"""Menu"""

# pygame modules are loaded dynamically, thus, supress no name/members errors
# pylint: disable=no-name-in-module
# pylint: disable=no-member
import pygame

BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)
pygame.init()


class Item(pygame.font.Font):
    """A simple menu item"""

    def __init__(self, text, pos_x=0, pos_y=0, font="Arial", size=60,
                 color=BLACK):
        self.font = pygame.font.SysFont(font, size)
        (self.text, self.function) = text
        self.color = color
        self.size = size
        self.label = self.font.render(self.text, 1, self.color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.position = (pos_x, pos_y)

    def set_position(self, pos_x, pos_y):
        """Sets position"""
        self.position = (pos_x, pos_y)

    def highlight(self, color):
        """Highlights an item"""
        self.color = color
        self.label = self.font.render(self.text, 1, self.color)

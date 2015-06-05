import pygame

from framework.input import InitialAction
from framework.state import State
from framework import input_manager

# pylint: disable=no-member
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


class MenuState(State):
    """State of Menu"""
    def __init__(self, width, height, texts):
        self.width = width / 2
        self.height = height / 2
        self.texts = texts
        self.items = []
        self.selected = 0

        for i, item in enumerate(self.texts):
            menu_item = Item(item)
            height = menu_item.height * len(self.texts)
            pos_x = self.width - menu_item.width / 2
            pos_y = self.height / 2 - height / 2 + i * 2 + 2 * i * menu_item.height
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.select_action = InitialAction()
        self.up_action = InitialAction()
        self.down_action = InitialAction()

    def resume(self):
        """Resumes the state"""
        input_manager.map_action(pygame.K_RETURN, self.select_action)
        input_manager.map_action(pygame.K_UP, self.up_action)
        input_manager.map_action(pygame.K_DOWN, self.down_action)
        input_manager.reset()

    def pause(self):
        """Pauses the state"""
        input_manager.clear()

    def handle_draw(self, canvas):
        """Sets color and menu items"""
        canvas.fill((40, 60, 190))
        for item in self.items:
            canvas.blit(item.label, item.position)
            item.highlight(BLACK)
        self.items[self.selected].highlight(CRIMSON)

    def handle_input(self, event):
        """Handles user input"""
        input_manager.handle_input(event)

    def handle_update(self, delta_time):
        """Updates the screen"""
        self.items[self.selected].highlight(BLACK)

        if self.up_action.active():
            self.selected = max(self.selected - 1, 0)

        if self.down_action.active():
            self.selected = min(self.selected + 1, len(self.items) - 1)

        self.items[self.selected].highlight(CRIMSON)

        if self.select_action.active():
            self.items[self.selected].function()

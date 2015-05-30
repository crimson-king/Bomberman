"""Options"""
import inspect
import pygame
from framework.state import State

BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)
pygame.init()


class OptionsState(State):
    """This is a state for options."""
    def __init__(self, width, height, items):
        self.width = width/2
        self.height = height/2
        self.items = items
        self.selected = 0

        for i, menu_item in enumerate(self.items):
            height = menu_item.height * len(self.items)
            pos_x = self.width - menu_item.width/2
            pos_y = self.height/2 - height/2 + i*2 + 2*i * menu_item.height
            menu_item.set_position(pos_x, pos_y)
    """Used for drawing and highlighting items."""
    def handle_draw(self, canvas):
        canvas.fill((40, 60, 190))
        for item in self.items:
            canvas.blit(item.label, item.position)
            item.highlight(BLACK)
        self.items[self.selected].highlight(CRIMSON)
    """Handles user input, browsing/selecting items in options menu"""
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.selected < len(self.items) - 1:
                    self.selected += 1
                else:
                    self.selected = 0
            elif event.key == pygame.K_UP:
                if self.selected == 0:
                    self.selected = len(self.items) - 1
                else:
                    self.selected -= 1
            elif event.key == pygame.K_RETURN:  # K_RETURN = enter
                function_spec = \
                    inspect.getfullargspec(self.items[self.selected].function)
                if len(function_spec[0]) == 1:
                    self.items[self.selected].function(self.items[0])
                else:
                    self.items[self.selected].function()
    """Unused method here."""
    def handle_update(self, delta_time):
        pass

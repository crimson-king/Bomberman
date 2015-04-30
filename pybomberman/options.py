import pygame
from framework.state import State
from pybomberman.menu import Item

BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)
pygame.init()


class OptionsState(State):
    def __init__(self, width, height, texts):
        self.width = width/2
        self.height = height/2
        self.texts = texts
        self.items = []
        self.selected = 0

        for i, item in enumerate(self.texts):
            menu_item = Item(item)
            height = menu_item.height * len(self.texts)
            x = self.width - menu_item.width/2
            y = self.height/2 - height/2 + i*2 + 2*i * menu_item.height
            menu_item.set_position(x, y)
            self.items.append(menu_item)

    def handle_draw(self, canvas):
        canvas.fill((40, 60, 190))
        for item in self.items:
            canvas.blit(item.label, item.position)
            item.highlight(BLACK)
        self.items[self.selected].highlight(CRIMSON)

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
                self.items[self.selected].function()

    def handle_update(self, dt):
        pass

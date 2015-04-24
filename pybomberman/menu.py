import pygame
from state import State

BLACK = (0, 0, 0)
pygame.init()


class Item(pygame.font.Font):
    def __init__(self, text, x=0, y=0, font="Arial", size=60,
                 color=BLACK):

        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.color = color
        self.size = size
        self.label = self.font.render(text, 1, self.color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.position = (x, y)

    def set_position(self, x, y):
        self.position = (x, y)


class MenuState(State):
    def __init__(self, width, height, texts):
        self.width = width/2
        self.height = height/2
        self.texts = texts
        self.items = []

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

    def handle_input(self, event):
        pass

    def handle_update(self, dt):
        pass




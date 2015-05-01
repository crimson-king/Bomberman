import pygame
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0x88, 0x88, 0))
        self.rect = self.image.get_rect()

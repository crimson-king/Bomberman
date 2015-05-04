import pygame
from pygame.sprite import Sprite

from pybomberman import PPM


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0x88, 0x88, 0))
        self.rect = self.image.get_rect()


class Wall(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PPM, PPM))
        self.image.fill((0, 0, 0xaa))
        self.rect = self.image.get_rect()

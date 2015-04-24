__author__ = 'Mateusz'

import pybomberman
from pybomberman.core import *
from pybomberman.state import *
from pybomberman.menu import *
import pygame

#print(pygame.font.get_fonts())
texts = ('Start', 'Options', 'Exit')
scr_width = 960
scr_height = 600
pybomberman.state.manager.push(MenuState(scr_width, scr_height, texts))
Game(handler=StateGameHandler()).start()
import pygame
import pygame.freetype as ft
from pygame.locals import *



WHITE = (255, 255, 255)
GREY =  (143, 143, 143)
BLACK = (  0,   0,   0)

class Dialog(object):
    def __init__(self, message, width=0, height=0,
                    text_color=WHITE, border_color=BLACK, background_color=GREY):

        self.message = message
        self.width = width
        self.height = height
        self.surface = self._build()

    def draw(self, surface, position=(0,0)):
        surface.blit(self.surface, position)

    def _build(self):
        message_surf = ft.Font.render(self.message)

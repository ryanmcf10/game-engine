import pygame, sys
import eventparser as ep
import env.overworld as overworld

from pygame.locals import *
from actions import *

def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300), RESIZABLE)
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("TEST")
    
    environment = overworld.Overworld('tests/maps/map1.tmx') 
    environment.add_player()

    actions = []

    while True:
        environment.update(DISPLAYSURF, actions)
        pygame.display.flip()

        actions = ep.parse_keymap(pygame.key.get_pressed())

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                environment.scale()
                #TODO: make this rescale the map instead of expanding display area
                DISPLAYSURF = pygame.display.set_mode((event.w, event.h), RESIZABLE)

        CLOCK.tick(30)

if __name__ == "__main__":
    main()

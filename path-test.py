import pygame, sys
import eventparser as ep
import env.overworld as overworld

from colors import *

from pygame.locals import *
from actions import *

def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("PATH TEST")
    
    environment = overworld.Overworld('tests/maps/test.tmx', debug=True) 
    

    actions = []

    while True:
        mouse_pos = list(pygame.mouse.get_pos())
        environment.debug_update(DISPLAYSURF, actions, mouse_pos)

        pygame.display.flip()

        actions = ep.parse_keymap(pygame.key.get_pressed())

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                environment.grid.toggle_cells()

        CLOCK.tick(30)

if __name__ == "__main__":
    main()

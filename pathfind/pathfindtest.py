import pygame, sys

from env.tools.grid import *
from pygame.locals import *
from colors import *

FPS = 30

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_COLS = 40
NUM_ROWS = 30

def main():
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    
    pygame.display.set_caption("GRID TEST")

    grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, NUM_COLS, NUM_ROWS, color=(255,255,255))

    DISPLAYSURF.blit(grid.image, (0, 0))
    
    while True:
        grid.update()
        pygame.display.flip()

        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(grid.image, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                grid.set_cell_value(grid.get_cell_at_point(mouse_pos), 1)

        CLOCK.tick(FPS)

if __name__ == '__main__':
    main()

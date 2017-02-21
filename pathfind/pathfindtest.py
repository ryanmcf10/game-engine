import pygame, sys

from env.tools.grid import *
from pygame.locals import *

FPS = 30

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_COLS = 40
NUM_ROWS = 30

def main():
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    
    pygame.display.set_caption("A* TEST")

    grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, NUM_COLS, NUM_ROWS, color=(255,255,255))

    highlight = pygame.Surface((grid.cell_width, grid.cell_height))
    highlight.fill((255,255,255,0.5))
    
    DISPLAYSURF.blit(grid.image, (0, 0))
    
    is_start_set = False
    is_goal_set = False

    start_pos = None
    goal_pos = None

    while True:
        pygame.display.flip()

        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(grid.image, (0,0))

        if is_start_set:
            pygame.draw.rect(DISPLAYSURF, (0,255,0), start_pos)
        if is_goal_set:
            pygame.draw.rect(DISPLAYSURF, (0,128,128), goal_pos)

        mouse_pos = pygame.mouse.get_pos()

        for rect in grid.grid_list:
            if rect.collidepoint(mouse_pos):
                DISPLAYSURF.blit(highlight, rect.topleft)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if not is_start_set:
                    is_start_set = True
                    for rect in grid.grid_list:
                        if rect.collidepoint(mouse_pos):
                            start_pos = rect
                            print("START: " + rect)
                elif not is_goal_set:
                    is_goal_set = True
                    for rect in grid.grid_list:
                        if rect.collidepoint(mouse_pos):
                            goal_pos = rect
                            print("GOAL: " + rect.)
        CLOCK.tick(FPS)

if __name__ == '__main__':
    main()

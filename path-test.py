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
            elif event.type == KEYDOWN:
                #toggle grid settings
                if event.key == K_1:
                    environment.grid.toggle_grid()
                elif event.key == K_2:
                    environment.grid.toggle_lines()
                elif event.key == K_3:
                    environment.grid.toggle_cells()

                #temporary -- set goal for pathfinding
                elif event.key == K_k:
                    current_cell = environment.grid.get_cell_at_grid_index(environment.goal)
                    goal = list(environment.goal)
                    goal[0] -= 1
                    environment.goal = tuple(goal)
                    environment.grid.set_cell_value(current_cell, current_cell.last_value)
                    environment.grid.set_cell_value(environment.grid.get_cell_at_grid_index(goal), 2)
                elif event.key == K_j:
                    current_cell = environment.grid.get_cell_at_grid_index(environment.goal)
                    goal = list(environment.goal)
                    goal[0] += 1
                    environment.goal = tuple(goal)
                    environment.grid.set_cell_value(current_cell, current_cell.last_value)
                    environment.grid.set_cell_value(environment.grid.get_cell_at_grid_index(goal), 2)
                elif event.key == K_h:
                    current_cell = environment.grid.get_cell_at_grid_index(environment.goal)
                    goal = list(environment.goal)
                    goal[1] -= 1
                    environment.goal = tuple(goal)
                    environment.grid.set_cell_value(current_cell, current_cell.last_value)
                    environment.grid.set_cell_value(environment.grid.get_cell_at_grid_index(goal), 2)
                elif event.key == K_l:
                    current_cell = environment.grid.get_cell_at_grid_index(environment.goal)
                    goal = list(environment.goal)
                    goal[1] += 1
                    environment.goal = tuple(goal)
                    environment.grid.set_cell_value(current_cell, current_cell.last_value)
                    environment.grid.set_cell_value(environment.grid.get_cell_at_grid_index(goal), 2)
                elif event.key == K_SPACE:
                    environment.handler.move_to(environment.goal)

        CLOCK.tick(30)

if __name__ == "__main__":
    main()

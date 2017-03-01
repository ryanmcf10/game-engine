from actions import *
import env.components.character
import env.tools.pathfinder as pf

OPPOSITES = [[UP, DOWN],
             [LEFT, RIGHT]]

"""
PLAYER ACTION HANDLER

Used to translate generic ACTIONS into movements/interactions for the player

=========================
INITIALIZATION PARAMETERS
=========================
character - Character object that will be manipulated

-------------------------
OPTIONAL
-------------------------
grid - Grid object that will be updated to reflect changes to the character
"""
class PlayerActionHandler(object):
    def __init__(self, character, grid=None):
        self.character = character
        self.grid = grid

        if grid is not None:
            self.graph = pf.WeightedGraph(self.grid)

    def execute(self, actions, blockers):
        is_running = False

        #check if the run modifier should be applied
        if MOD in actions:
            is_running = True
            actions.remove(MOD)

        #check if interactions should be handled
        if SELECT in actions:
            actions.remove(SELECT)

        #check for movement
        #TODO -- handle collisions better
        if len(actions) > 0:
            if self.grid:
                self._move_and_update_grid(actions, is_running, blockers)            
            else:
                self._move(actions, is_running, blockers)
        else:
            self.character.pause()

    def _move_and_update_grid(self, directions, mod, blockers):
        current_cell = self.grid.get_cell_at_point(self.character.collision_rect.center)

        self._move(directions, mod,blockers)

        updated_cell = self.grid.get_cell_at_point(self.character.collision_rect.center)

        if current_cell != updated_cell:
            self.grid.set_cell_value(current_cell, current_cell.last_value)
            self.grid.set_cell_value(updated_cell, 2)

    def _move(self, directions, mod, blockers):
        self.character.move(directions, is_running=mod)


    def move_to(self, goal):
        start = self.grid.get_cell_at_point(self.character.collision_rect.center).position
        came_from, cost_so_far = pf.a_star_search(self.graph, start, goal)
        print(pf.reconstruct_path(came_from, start, goal))
        for index in pf.reconstruct_path(came_from, start, goal):
            current_cell = self.grid.get_cell_at_grid_index(index)
            self.grid.set_cell_value(current_cell, 3)
       
class NpcActionHandler(object):
    def __init__(self, character):
        self.character = character

    def execute():
        pass

import pygame
import env.tools.grid as grid

"""
MAP
"""
class Map():
    def __init__(self, width, height, num_cols, num_rows, map_data, map_format):
        #metadata about the size of the map
        self.width = width
        self.height = height
        self.num_cols = num_cols
        self.num_rows = num_rows

        self.map_format = map_format
        self.map_data = map_data

        #surface containg grid outline for the map
        self.grid = grid.Grid(width, height, num_cols, num_rows)

        self._build_blockers()

    """
    Temporary solution to build the blockers on the map
    """
    def _build_blockers(self):
        self.blockers = []

        for object in self.map_data.objects:
            properties = object.__dict__
            blocker = pygame.Rect(object.x, object.y, object.width, object.height)

            if properties['name'] == 'blocker':
                self.blockers.append(blocker)

                #print("\n================")
                #print("OBJECT ID: {}".format(str(properties['id'])))
                #print("================")
                 
                #self.grid.set_cell_value(self.grid.get_cell_at_point(blocker.center), 1)
                cells = self.grid.get_cells_in_rect(blocker)

                for cell in cells:
                    self.grid.set_cell_value(cell, 1)

import pygame.sprite
from colors import *

"""
GRID

A grid of Cells, used to represent the value of each tile on a map
Used for path finding.

=========
INITIALIZATION PARAMETERS
=========
width - int - width of the grid in pixels
height - int - height of the grid in pixels
num_rows - int - number of rows in the grid
num_cols - int - number of columns in the grid

OPTIONAL
----------
color - (R, G, B) - color of the grid as a valid RGB value

"""
class Grid(pygame.sprite.Sprite):
    def __init__(self, width, height, num_cols, num_rows, color=(0,0,0)):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.color = color
        
        self.cell_width = width/num_cols
        self.cell_height = height/num_rows
    
        self.show_lines = True
        self.show_cells = True

        self._init_grid_data()

        #set self.image
        self._draw_grid()

        #need rect to keep track of grid position
        self.rect = self.image.get_rect()

        self.is_up_to_date = True

    def update(self):
        if not self.is_up_to_date:
            self._draw_grid()
            self.is_up_to_date = True

    #initialize a 2D array of cells
    def _init_grid_data(self):
        self.grid_data = [[Cell(0, pygame.Rect(y*self.cell_width, x*self.cell_height, self.cell_width, self.cell_height), x, y) for y in range(self.num_cols)] for x in range(self.num_rows)]

    #draw the grid data to a surface and set as the grid's image
    # EXPENSIVE
    def _draw_grid(self):
        grid_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for x in range(self.num_rows):
            for y in range(self.num_cols):
                current_cell = self.grid_data[x][y]

                if self.show_cells:
                    if current_cell.value == 1:
                        temp = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA)
                        temp.convert_alpha()
                        temp.fill((255,0,0,128))

                        grid_surface.blit(temp, (y*self.cell_width, x*self.cell_height))

                if self.show_lines:
                    pygame.draw.rect(grid_surface, self.color, current_cell.rect, 1)

        self.image = grid_surface

    """
    Set the color of the grid lines and set teh update flag

    :param: color - (R,G,B) tuple
    """
    def set_color(self, color):
        self.color = color
        self.is_up_to_date = False

    """
    Set the cell to a value and set the update flag

    :param: cell - cell to update
    :param: value - value to set cell to
    """
    def set_cell_value(self, cell, value):
        cell.value = value
        self.is_up_to_date = False
    

    """
    Set the value of all cells in a list and set the update flag

    :param: cells - list of cells
    :param" value - value to set cells to
    """
    def set_cell_values(self, cells, value):
        assert type(cells) is list, "set_cell_value: parameter 'cells' must be of type list."
        for cell in cells:
            cell.value = value
        self.is_up_to_date = False

    """
    Get the cell at a certain point on the map

    ?? make this a better search ??

    :param: position - (x,y) list or tuple
    :return: result - Cell, or none
    """
    def get_cell_at_point(self, position):
        result = None

        x_cord = position[0]
        y_cord = position[1]

        for x in range(self.num_rows):
            top = self.grid_data[x][0].rect.top
            bottom = self.grid_data[x][0].rect.bottom

            if y_cord > top and y_cord <= bottom:
                for y in range(self.num_cols):
                    left = self.grid_data[x][y].rect.left
                    right = self.grid_data[x][y].rect.right

                    if x_cord > left and x_cord <= right:
                        result = self.grid_data[x][y]

        return result

    """
    Get all cells touching a rectangle

    :param: rect - pygame.Rect bounding rectangle
    :return: result - list of cells
    """
    def get_cells_in_rect(self, rect):
        result = []

        x_start = rect.topleft[0]
        y_start = rect.topleft[1]

        x_end = rect.bottomright[0]
        y_end = rect.bottomright[1]

        starting_row = 0
        starting_col = 0
        ending_row = 0
        ending_col = 0

        for x in range(self.num_rows):
            top = self.grid_data[x][0].rect.top
            bottom = self.grid_data[x][0].rect.bottom

            if y_start > top and y_start <= bottom:
                starting_row = x

                for y in range(self.num_cols):
                    left = self.grid_data[x][y].rect.left
                    right = self.grid_data[x][y].rect.right

                    if x_start > left and x_start <= right:
                        starting_col = y

            if y_end > top and y_end <= bottom:
                ending_row = x
                
                for y in range(self.num_cols):
                    left = self.grid_data[x][y].rect.left
                    right = self.grid_data[x][y].rect.right

                    if x_end > left and x_end <= right:
                        ending_col = y

        print("Starting row: {}  Ending row: {}".format(starting_row, ending_row))
        print("Starting col: {}  Ending col: {}".format(starting_col, ending_col))
        for row in range(starting_row, ending_row+1):
            current_row = self.grid_data[row+1]
            for col in range(starting_col, ending_col):
                result.append(current_row[col+1])

        return result

    def toggle_lines(self):
        self.show_lines = not self.show_lines
        self.is_up_to_date = False

    def toggle_cells(self):
        self.show_cells = not self.show_cells
        self.is_up_to_date = False

"""
CELL

One unit in a grid.

Contains a value (int) and a pygame.Rect to hold its position
"""
class Cell():
    def __init__(self, value, rect, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.rect = rect
        self.position = (row, col)

    def __repr__(self):
        return "<Cell> Row: {}  Col: {}  Value: {}".format(self.row, self.col, self.value)

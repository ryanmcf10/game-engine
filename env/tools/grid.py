import pygame.sprite

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

        self.grid_list = []
        self.grid_values = [[0]*num_cols]*num_rows

        self.image = self._init_grid()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def _init_grid(self):
        grid_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                rect = pygame.Rect(col*self.cell_width, row*self.cell_height, self.cell_width, self.cell_height)
                self.grid_list.append(rect)

                pygame.draw.rect(grid_surface, self.color, rect, 1)

        return grid_surface


    def highlight_cell(self, position):
        temp = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA, 32)
        temp.convert_alpha()
        temp.fill((255, 255, 255))

        for cell in self.grid_list:
            if cell.collidepoint(position):
                self.image.blit(temp, cell.topleft)

class Cell():
    def __init__(self, row, col, width, height, position):
       self.row = row
       self.col = col
       self.rect = pygame.Rect(col*width, row*height, width, height)

    def __repr__(self):
        return "<Cell>\nRow: {}  Col: {}".format(self.row, self.col)

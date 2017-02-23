from env import environmentabc as environmentabc
import env.tools.camera as camera
import env.tools.maploader as maploader
import env.tools.actionhandler2 as actionhandler
import env.components.character as character
import env.components.npc as npc
from env.tools.grid import *

from actions import *

class Overworld(environmentabc.Environment):
    def __init__(self, filename, debug=False):
        self.debug = debug

        self.map = maploader.load_map_tmx(filename)

        self.view = camera.ScrollingCamera(self.map.map_data, screensize=(400,300)) 

        self.add_player()
        self.position = [300, 150]

        if self.debug:
            self._show_grid()

    def update(self, surface, actions):
        position = self.player.position

        self.view.update()
        self.view.draw(surface, position)

        self.handler.execute(actions, self.map.blockers)

    def scale(self):
        pass

    def add_player(self):
        anim_dict = {UP:[2, 1, 0, 2, 3, 4],
                     DOWN:[10, 9, 8, 10, 11, 12],
                     RIGHT:[16, 17, 18, 16, 21, 22],
                     LEFT:[24, 25, 26, 24, 29, 30]}

        self.player = character.OverworldCharacter('./tests/characters/sprites/male_sprite_model.png', position=[300,150],
                                                    num_rows=4, num_cols=8, default_image=10, animation_dictionary=anim_dict,
                                                    display_time=100, debug=self.debug)

        self.view.add(self.player)
        self.handler = actionhandler.PlayerActionHandler(self.player)

    def _calc_mouse_vector(self, mouse_pos):
        center = [200, 150]
        x_vector = mouse_pos[0] - center[0]
        if abs(x_vector) < 50:
            x_vector = 0
        y_vector = mouse_pos[1] - center[1]
        if abs(y_vector) < 50:
            y_vector = 0

        mouse_vector = [x_vector, y_vector]
        return mouse_vector
    
    def _calc_position(self, mouse_pos):
        mouse_vector = self._calc_mouse_vector(mouse_pos)

        self.position[0] += mouse_vector[0]/20
        if self.position[0] <= 0:
            self.position[0] = 0
        elif self.position[0] >= self.map.width:
            self.position[0] = self.map.width

        self.position[1] += mouse_vector[1]/20
        if self.position[1] <= 0:
            self.position[1] = 0
        elif self.position[1] >= self.map.height:
            self.position[1] = self.map.height

    def debug_update(self, surface, actions, mouse_pos):
        self._calc_position(mouse_pos)

        self.view.update()
        self.view.draw(surface, self.position)
        blocks = self.map.blockers
        self.handler.execute(actions, blocks)

    def _show_grid(self):
        self.grid = self.map.grid
        self.view.add_grid(self.grid)

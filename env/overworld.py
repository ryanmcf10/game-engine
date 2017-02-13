from env import environmentabc as environmentabc
import env.tools.camera as camera
import env.tools.maploader as maploader
import env.tools.actionhandler as actionhandler
import env.components.character as character
from actions import *

class Overworld(environmentabc.Environment):
    def __init__(self, filename):
        self.map = maploader.MapLoader(filename)

        self.view = camera.ScrollingCamera(self.map.mapfile, screensize=(400,300)) 

        anim_dict = {UP:[2, 1, 0, 2, 3, 4],
                     DOWN:[10, 9, 8, 10, 11, 12],
                     RIGHT:[16, 17, 18, 16, 21, 22],
                     LEFT:[24, 25, 26, 24, 29, 30]}

        #self.player = character.OverworldCharacter('./tests/characters/sprites/me.jpg', position=[200,150])
        self.player = character.OverworldCharacter('./tests/characters/sprites/male_sprite_model.png', position=[300,150],
                                                    num_rows=4, num_cols=8, default_image=10, animation_dictionary=anim_dict,
                                                    display_time=100) 
        self.view.add(self.player)

    def update(self, surface, actions):
        actionhandler.handle_character_movement(actions, self.player, self.map.blockers)
        self.view.update()
        position = self.player.position
        self.view.draw(surface, position)

    def scale(self):
        pass

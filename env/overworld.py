from env import environmentabc as environmentabc
import env.tools.camera as camera
import env.tools.maploader as maploader
import env.tools.actionhandler2 as actionhandler
import env.components.character as character
import env.components.npc as npc

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

        self.npc_collection = npc.NpcCollection()

        char1 = character.OverworldCharacter('./tests/characters/sprites/female_sprite_model.png', position=[0,0],
                                                    num_rows=4, num_cols=8, default_image=10, animation_dictionary=anim_dict,
                                                    display_time=100)
        self.npc_collection.add(char1)

        char2 = character.OverworldCharacter('./tests/characters/sprites/child_sprite_model.png', position=[400, 300],
                                                    num_rows=4, num_cols=8, default_image=10, animation_dictionary=anim_dict,
                                                    display_time=100)

        self.npc_collection.add(char2)


        for npc in self.npc_collection.npc_list:
            self.view.add(npc)

        self.view.add(self.player)
        self.handler = actionhandler.PlayerActionHandler(self.player)

    def update(self, surface, actions):
        position = self.player.position
        self.view.update()
        self.view.draw(surface, position)


        blocks = self.npc_collection.get_rects() + self.map.blockers

        self.handler.execute(actions, blocks)
        
    def scale(self):
        pass

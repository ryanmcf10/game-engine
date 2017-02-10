from env import environmentabc as environmentabc
from env.tools import camera as camera
from env.tools import maploader as maploader
from env.components import character as character
from actions import *

class Overworld(environmentabc.Environment):
    def __init__(self, filename):
        self.map_loader = maploader.MapLoader()
        self.current_map = self.map_loader.load_map(filename)
        self.view = camera.ScrollingCamera(self.current_map, screensize=(400,300)) 

        anim_dict = {UP:[2, 1, 0, 2, 3, 4],
                     DOWN:[10, 9, 8, 10, 11, 12],
                     RIGHT:[16, 17, 18, 16, 21, 22],
                     LEFT:[24, 25, 26, 24, 29, 30]}

        #self.player = character.OverworldCharacter('./tests/characters/sprites/me.jpg', position=[200,150])
        self.player = character.OverworldCharacter('./tests/characters/sprites/male_sprite_model.png', position=[200,150], num_rows=4, num_cols=8, default_image=10, animation_dictionary=anim_dict, display_time=10) 
        self.view.add(self.player)

    def update(self, surface, actions):
        self.handle_actions(actions)
        self.view.update()
        position = self.player.position
        self.view.draw(surface, position)

    def scale(self):
        pass

    def handle_actions(self, actions):
        if len(actions) == 0:
            self.player.pause()
        else:
            self.player.play()
            for action in actions:
                if action == UP:
                    self.player.moveup()
                elif action == DOWN:
                    self.player.movedown()
                elif action == RIGHT:
                    self.player.moveright()
                elif action == LEFT:
                    self.player.moveleft()

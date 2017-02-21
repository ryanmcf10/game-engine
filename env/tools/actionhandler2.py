from actions import *
import env.components.character

OPPOSITES = [[UP, DOWN],
             [LEFT, RIGHT]]

class PlayerActionHandler(object):
    def __init__(self, character):
        self.character = character

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
            self.character.move(actions, is_running)

            if self.character.is_collision(blockers):
                self.character.move_back()
        else:
            self.character.pause()

class NpcActionHandler(object):
    def __init__(self, character):
        self.character = character

    def execute():
        pass

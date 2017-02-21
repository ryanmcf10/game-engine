from actions import *

"""
Convert a list of actions into corresponding movments by the character

If the actions list contains movements, the character will move animate.
If the actions list contains no movement instructions, it will display the default image.

:param: actions - list of actions tobe performed
:param: character - character to perform the actions
"""
def handle_character_movement(actions, character, blockers):
    is_running = False

    if MOD in actions:
        is_running = True
        actions.remove(MOD)

    if SELECT in actions:
        actions.remove(SELECT)

    if len(actions) > 0:
        character.move(actions, run=is_running)
        if _is_character_colliding_with_blockers(blockers, character):
            print('COLLISION')
            character.moveback()

    else:
        character.default()

"""
Check if the character is colliding with any of the blockers in the world
Returns True if it is colliding, false if no collision

:param: blockers - list of all blockers in the current map
:param: character - character to check collisions for
"""
def _is_character_colliding_with_blockers(blockers, character):
    if character.rect.collidelist(blockers) == -1:
        return False
    else:
        return True

def move_back(actions, character):
    pass

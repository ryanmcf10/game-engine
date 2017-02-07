from actions import *
from pygame.locals import *

"""
parse a keymap to get actions to be performed before next update

:param: keymap - current state of all keys
:return: actions - list of actions to be performed on next update
"""
def parse_keymap(keymap):
    actions = []

    if(keymap[K_LSHIFT]):
        actions.append(MOD)

    if(keymap[K_UP] or keymap[K_w]):
        actions.append(UP)

    if(keymap[K_DOWN] or keymap[K_s]):
        actions.append(DOWN)

    if(keymap[K_LEFT] or keymap[K_a]):
        actions.append(LEFT)

    if(keymap[K_RIGHT] or keymap[K_d]):
        actions.append(RIGHT)

    if(keymap[K_SPACE] or keymap[K_RETURN]):
        actions.append(SELECT)

    #if opposite actions are to be performed, cancel them out (eg cannot contain UP and DOWN)
    if(len(actions) > 1):
        pairs = [[UP, DOWN],
                [LEFT, RIGHT]]

        for pair in pairs:
            if set(pair).issubset(actions):
                #remove the opposite actions from the actions list
                actions = [action for action in actions if action not in pair]

    return actions


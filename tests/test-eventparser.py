#allow loading module from parent directory
import sys
sys.path.insert(0, '..')

#import test framework and module to be tested
import unittest
import eventparser as ep

#import constants
from pygame.locals import *
from actions import *

class EventParserTestCase(unittest.TestCase):

    def test_returns_correct_action(self):
        """Are keypresses turned into correct actions?"""
        #create dictionary of actions and corresponding keypresses
        mappings = {UP:[K_UP, K_w],
                    DOWN:[K_DOWN, K_s],
                    LEFT:[K_LEFT, K_a],
                    RIGHT:[K_RIGHT, K_d],
                    MOD:[K_LSHIFT],
                    SELECT:[K_SPACE, K_RETURN]}

        #loop over all items in the mappings dictionary and make sure keypresses map to correct action
        for action, inputs in mappings.items():
            for keypress in inputs:
                #arrange
                keymap = self.initialize_blank_keymap()
                keymap[keypress] = 1 

                #act
                result = ep.parse_keymap(keymap)

                #assert
                self.assertEqual([action], result, msg="Returned action list varies from expected action list for action: {} and key {}".format(action, keypress))

    def test_opposite_actions_cancel(self):
        """Do opposite actions (ie UP/DOWN, LEFT/RIGHT) cancel out in the action list?"""
        mappings = [[K_UP, K_DOWN],
                    [K_LEFT, K_RIGHT]]

        #loop over all opposite pairs and test
        for pair in mappings:
            #arrange
            keymap = self.initialize_blank_keymap()
            for keypress in pair:
                keymap[keypress] = 1
            
            #act
            result = ep.parse_keymap(keymap)

            #assert
            self.assertEqual([], result, msg="Returned action list is not empty for keys: {} and {}".format(pair[0], pair[1]))


    def initialize_blank_keymap(self):
        return [0]*323

if __name__ == "__main__":
    unittest.main()

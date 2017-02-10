import os
import pygame.sprite
import pyganim
from actions import *

MOVEMENT_SPEED = 9

class OverworldCharacter(pygame.sprite.Sprite):
    """
    OVERWORLD CHARACTER

    Basic representation of an animated sprite in the overworld


    =========================
    INITIALIZATION PARAMETERS
    =========================

    sprite_sheet - sprite sheet image that will be used to display character
    
    position - [x, y] coordinates for starting position of character

    num_rows, num_cols - number of rows and columns on the sheet. Used to slice the sprite sheet into individual frames.
                        !! Frames are numbered in order from top left to bottom right, starting from 0:
                            eg:
                                    0   1   2   3   4
                                    5   6   7   8   9
                                    10  11  12  13  14

                        !! If num_rows and num_cols are not specified, the sprite sheet will not be gridded
    
    default_image - the image that will be displayed when 'current_animation' is None

    animation_dictionary - dictionary to explain which frames correspond to a given action
                           frames should be listed in the order that they are to be played

                            eg:
                                {'UP':[0, 1, 2, 3, 4],
                                 'DOWN':[5, 6, 7, 8, 9],
                                 'LEFT':[10, 11, 12, 13],
                                 'RIGHT':[14, 15, 16, 17]}

    current_animation - the animation that is currently playing --  set to None to display 'default_image' 

    direction - the direction that the sprite is currently facing
    """
    def __init__(self, sprite_sheet, position, num_rows=1, num_cols=1,
                    default_image=0, animation_dictionary=None, display_time=100,
                    direction=DOWN, current_action=None):

        pygame.sprite.Sprite.__init__(self)

        self.position = position

        #split the spritesheet into a list of individual images
        self._images = pyganim.getImagesFromSpriteSheet(sprite_sheet, rows=num_rows, cols=num_cols)

        #set the character to show the default image
        #if num_cols or num_rows is not supplied, _images will only be a pygame Surface, not a list
        if type(self._images) is list:
            self.image = self._images[default_image]
            self.is_animated = True
        else:
            self.image = self._images
            self.is_animated = False

        self.current_action = current_action
        self.direction = direction
        self.rect = self.image.get_rect()

        #take the animation dictionary and convert it to Pyganim animations for each action
        if(animation_dictionary):
            self.animations = self.build_animations(animation_dictionary, display_time)
            self._move_conductor = pyganim.PygConductor(self.animations)
                
    #update the postion of the character.  updates the animation frame if necessary
    def update(self):
        if self.current_action and self.is_animated:
            self._update_animation() 

        self.rect.topleft = self.position

    #methods to handle character movement and set animation flags
    def moveup(self):
        self.position[1] -= MOVEMENT_SPEED
        if self.current_action == None:
            self.current_action = UP
            self.direction = UP

    def movedown(self):
        self.position[1] += MOVEMENT_SPEED
        if self.current_action == None:
            self.current_action = DOWN
            self.direction = DOWN

    def moveleft(self):
        self.position[0] -= MOVEMENT_SPEED
        self.current_action = LEFT
        self.direction = LEFT

    def moveright(self):
        self.position[0] += MOVEMENT_SPEED
        self.current_action = RIGHT
        self.direction = RIGHT

    def _update_animation(self):
        temp = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA, 32)
        temp.convert_alpha()

        self.animations[self.current_action].blit(temp, (0,0))
        self.image = temp
        
    def pause(self):
        self._move_conductor.pause()
        self.current_action = None

    def play(self):
        self._move_conductor.play()

    """
    Build a dictionary of actions and pyganim animations
    By default, all animations are paused.

    Called when the class is constructed and passed an 'animation_dictionary'

    Ex:
        {UP:<walk up animation>,
         DOWN:<walk down animation>,
         LEFT:<walk left animation>,
         RIGHT:<walk right animation>}

    """
    def build_animations(self, animation_dictionary, display_time):
        assert type(animation_dictionary) is dict, "Animation dictionary must be a dictionary {key=Action:value=[List of images]}"
        animations = {}

        for action, image_list in animation_dictionary.items():
            images = []
            for image in image_list:
                images.append(self._images[image])

                if image == self.image:
                    self.current_action = DOWN

            display_times = [display_time]*len(images)

            images = list(zip(images, display_times))
            animation = pyganim.PygAnimation(images)

            animations[action] = animation

        return animations

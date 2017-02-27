import os
import pygame.sprite
import pyganim
from actions import *

class Character():
    """
    CHARCTER

    The main representation of a character

    The Character contains metadata/state, and is composed of specific representations of a character for different game environments.
    
    """
    def __init__(self):
        pass

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

    direction - the direction that the sprite is currently facing

    !! nedded to crete an animated sprite
    animation_dictionary - dictionary to explain which frames correspond to a given action
                           frames should be listed in the order that they are to be played

                            eg:
                                {'UP':[0, 1, 2, 3, 4],
                                 'DOWN':[5, 6, 7, 8, 9],
                                 'LEFT':[10, 11, 12, 13],
                                 'RIGHT':[14, 15, 16, 17]}

    display_time - the amount of time each frame in an animation should be displayed for

    current_action - the animation that is currently playing --  set to None to display 'default_image' 
    """

    def __init__(self, sprite_sheet, position, num_rows=1, num_cols=1,
                    default_image=0, animation_dictionary=None, display_time=100,
                    direction=DOWN, current_action=None, movement_speed=5, run_modifier=1.5,
                    debug=False):

        pygame.sprite.Sprite.__init__(self)

        self.position = position
        self.last_position = position
        self.movement_speed = movement_speed
        self.run_modifier = run_modifier
        self.is_moving = False

        #split the spritesheet into a list of individual images
        self._images = pyganim.getImagesFromSpriteSheet(sprite_sheet, rows=num_rows, cols=num_cols)

        #set the character to show the default image
        #if num_cols or num_rows is not supplied, _images will only be a single pygame Surface, not a list
        if type(self._images) is list:
            self.image = self._images[default_image]
            self.is_animated = True
        else:
            self.image = self._images
            self.is_animated = False

        self.current_action = current_action
        self.direction = direction
        
        #used for drawing the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        #used to check for collisions
        self.collision_rect = pygame.Rect(0, 0, self.rect.width * .5, 8)
        self.collision_rect.midbottom = self.rect.midbottom

        #take the animation dictionary and convert it to Pyganim animations for each action
        if(animation_dictionary):
            self.animations = self._build_animations(animation_dictionary, display_time)
            self._move_conductor = pyganim.PygConductor(self.animations)

        self.debug = debug
  
    #update the postion of the character.  updates the animation frame if necessary
    def update(self):
        if self.current_action and self.is_animated:
            self._update_animation() 

    #set the character to display the next frame of the animation
    def _update_animation(self):
        assert self.is_animated, "Character must be animated in order to call this method"
        temp = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA, 32)
        temp.convert_alpha()

        #set the sprites image

        if self.debug:
            #fill the sprite with transparent green
            temp.fill((0,255,0,128))

            self.animations[self.current_action].blit(temp, (0,0))

            #display the collision rect in transparent red
            collision_rect = pygame.Surface((self.collision_rect.width, self.collision_rect.height), pygame.SRCALPHA)
            collision_rect.convert_alpha()
            collision_rect.fill((255,0,0,128))
            temp.blit(collision_rect, (8,56))

        else:
            self.animations[self.current_action].blit(temp, (0,0))

        self.image = temp
        
    #figure out which way the sprite should be facing
    def _set_direction(self, directions):
        assert self.is_animated, "Character must be animated in order to call this method"
        if LEFT in directions or RIGHT in directions:
            self.direction = list((set([LEFT, RIGHT]) & set(directions)))[0] 
        else:
            self.direction = list((set([UP, DOWN]) & set(directions)))[0]

        self.current_action = self.direction

    #move the position of the sprite in the specified directions
    def move(self, directions, is_running=False):
        self._move_conductor.play()
        self._set_direction(directions)

        self.last_position = self.position[:]

        speed = self.movement_speed

        if is_running:
            speed = int(speed * self.run_modifier)

        for direction in directions:
            if direction == UP:
                self.position[1] -= speed
            elif direction == DOWN:
                self.position[1] += speed
            elif direction == LEFT:
                self.position[0] -= speed
            elif direction == RIGHT:
                self.position[0] += speed

        self.rect.topleft = self.position
        self.collision_rect.midbottom = self.rect.midbottom

    #undo the last move
    def move_back(self):
        self.position = self.last_position[:]
        self.rect.topleft = self.position
        self.collision_rect.midbottom = self.rect.midbottom

    #called by the action handler if no actions are to be performed
    def pause(self):
        assert self.is_animated, "Character must be animated in order to call this method"
        self._move_conductor.pause()
        self.current_action = None

        temp = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA, 32)
        temp.convert_alpha()


        if self.debug:
            #fill the sprite with tranparent green
            temp.fill((0,255,0,128))

            temp.blit(self.animations[self.direction].getFrame(0), (0,0))

            #fill the collision rect with transparent red
            collision_rect = pygame.Surface((self.collision_rect.width, self.collision_rect.height), pygame.SRCALPHA)
            collision_rect.convert_alpha()
            collision_rect.fill((255,0,0,128))
            temp.blit(collision_rect, (8,56))

        self.image = temp

    def is_out_of_bounds(self, max_x, max_y):
        return self.rect.top < 0 or self.rect.left < 0 or self.rect.bottom > max_y or self.rect.right > max_x
        
    #check if the character is colliding with any rects in the blockers list
    def is_collision(self, blockers):
        assert type(blockers) is list, "Blockers must be a list of pygame.Rect objects"
        return self.collision_rect.collidelist(blockers) != -1

    def draw_collision_rect(self):
        temp = pygame.Surface((self.collision_rect.width, self.collision_rect.height), pygame.SRCALPHA)
        temp.fill((255,0,0))
        self.image.blit(temp, self.collision_rect.topleft)

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
    def _build_animations(self, animation_dictionary, display_time):
        assert type(animation_dictionary) is dict, "Animation dictionary must be a dictionary {key=Action:value=[List of images]}"
        animations = {}

        for action, image_list in animation_dictionary.items():
            images = []
            for image in image_list:
                images.append(self._images[image])

            display_times = [display_time]*len(images)

            images = list(zip(images, display_times))
            animation = pyganim.PygAnimation(images)

            animations[action] = animation

        return animations

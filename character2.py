import pygame.sprite
import pyganim

from abc import ABCMeta, abstractmethod

from actions import *
from colors import *

class Character:
    def __init__(self):
        self.width = 10
        self.height = 10

        self.collision_rect = pygame.Rect((100,100), (100,100))

class OverworldCharacter(pygame.sprite.Sprite):
    """
    OVERWORLD CHARACTER

    Representation of a character sprite in the overworld.

    =========================
    Initialization Parameters
    =========================

    sprite - pygame.Image object or string path to where the image is located

    position - list of [x,y] coordinates for the character's starting position

    movement_speed - how fast the sprite moves in pixels/frame

    run_modifier - multiplier to calculate movement_speed when running

    debug - Use debug methods

    """
    def __init__(self, sprite, position, movement_speed=6, run_modifier=1.5, debug=False):

        pygame.sprite.Sprite.__init__(self)

        self.position = position
        self.last_position = position

        self.movement_speed = movement_speed
        self.run_modifier = run_modifier

        # set the display image of the character
        if type(sprite) is str:
            self.image = pygame.image.load(sprite)
        else:
            self.image = sprite

        # position rect
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        # collision rect
        self.collision_rect = pygame.Rect(0, 0, self.rect.width*.5, 8)
        self.collision_rect.midbottom = self.rect.midbottom

        self.width = self.rect.width
        self.height = self.rect.height

        # used for drawing the image
        self.current_frame = self.image

        # used to determine how to call methods at runtime
        if debug:
            self.state = OverworldDebugState(self)
        else:
            self.state = OverworldState(self)

    """
    Call the draw function based on whether in debug mode or not
    """
    def draw(self):
        self.state.draw()

    """
    Move the character in the given directions.

    If a list of blockers is supplied, checks if the movement is valid.
    
    :param: directions - list of directions (UP, DOWN, LEFT, RIGHT)
    :param: blockers - list of pygame.Rect objects
    :param: is_running - apply the run_modifier to movement_speed?
    """
    def move(self, directions, blockers=None, is_running=False):  
        speed = self.movement_speed

        if is_running:
            speed = int(speed * self.run_modifier)

        for direction in directions:
            self.last_position = self.position[:]

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

            # if provided with a list of blockers, check for a collision
            if blockers and self.is_collision(blockers):
                self.move_back()

    def move_back(self):
        self.position = self.last_position[:]
        self.rect.topleft = self.position
        self.collision_rect.midbottom = self.rect.midbottom

    def is_collision(self, blockers):
        return self.collision_rect.collidelist(blockers) != -1

class AnimatedOverworldCharacter(OverworldCharacter):
    """
    ANIMATED OVERWORLD CHARACTER

    Animated version of an overworld character.

    =========================
    Initialization Parameters
    =========================

    sprite_sheet - string path to the sprite sheet for the character

    num_rows, num_cols - number of rows and columns of the sprite sheet.  Used to slice the spritesheet into individual images.
                            !! Images are numbered from top left to bottom right, starting from 0
                                eg: num_rows = 4, num_cols = 6

                                    0   1   2   3   4   5
                                    6   7   8   9   10  11
                                    12  13  14  15  16  17
                                    18  19  20  21  22  23

    position - list of [x,y] coordinates for the chacter's starting position

    direction - which direction the sprite is facing (UP, DOWN, LEFT, RIGHT)

    default_image - which image from the spritesheet should be used first

    animation_dictionary - dictionary to explain which images from the spritesheet correspond to a given action
                            images should be listed in the order that they are to be displayed
                            {ACTION:[list of images]}

                            eg:
                                {UP:[0,1,2,3,2,1],
                                 DOWN:[5,6,7,8,9,10],
                                 LEFT:[11,12,13,14,13,12],
                                 JUMPLEFT:[14,15,16,15],
                                 SWINGSWORD:[19,20,21,22,23]}

    display_time - the amount of time each frame should be displayed for in milliseconds
                    100 is a reasonable default

    movement_speed - the speed at which the character will move in the overworld, in pixels/frame

    run_modifier -  modifier to calculate movement_speed when running

    current_animation - which animation from the dictionary to display when the sprite is initialized

    debug - determine how to draw the sprite
    """
    def __init__(self, sprite_sheet, position, num_rows, num_cols, default_image=0, direction=DOWN,
                    animation_dictionary=None, display_time=100, movement_speed=6, run_modifier=1.5,
                    current_animation=None, debug=False):
       
        # split the sprite sheet into a list of individual images
        self._images = pyganim.getImagesFromSpriteSheet(sprite_sheet, rows=num_rows, cols=num_cols)
        
        # call the constructor of the base class
        super(AnimatedOverworldCharacter, self).__init__(self._images[default_image], position, movement_speed, run_modifier, debug)

        self.direction = direction

        self.current_animation = current_animation

        self.animations = self._build_animation_dictionary(animation_dictionary, display_time)
        
        # used to play/pause animations and keep them in sync
        self.animation_conductor = pyganim.PygConductor(self.animations)

        self.current_frame = self.image

    """
    Move the sprite, and also set the direction of the sprite and play the animation for movement in that direction

    :param: directions - list of directions (UP, DOWN, LEFT, RIGHT)
    :param: blockers - list of pygame.Rect objects
    :param: is_running - apply the run_modifier to movement_speed
    """
    def move(self, directions, blockers=None, is_running=False):
        super(AnimatedOverworldCharacter, self).move(directions, blockers, is_running)
        self._determine_direction(directions)
        self.current_animation = self.direction
        self.animation_conductor.play()

    """
    If there is no animation to play, pause the animation conductor
    """
    def pause(self):
        self.current_animation = None
        self.animation_conductor.pause()

    """
    Set the current_frame to the image that should be drawn on next update
    """
    def update(self):
        if self.current_animation:
            self.current_frame = self.animations[self.current_animation].getCurrentFrame()
        else:
            self.current_frame = self.animations[self.direction].getFrame(0)

    """
    Determines and sets the current direction that the sprite should be facing, given the directions that it is currently moving

    :param: directions - list of directions (UP, DOWN, LEFT, RIGHT)
    """
    def _determine_direction(self, directions):
        if LEFT in directions or RIGHT in directions:
            self.direction = list((set([LEFT, RIGHT]) & set(directions)))[0]
        else:
            self.direction = list((set([UP, DOWN]) & set(directions)))[0]

    """
    Build a dictionary of ACTIONs and PygAnim animations.
    By default, all animations are paused.

    Called when the class is constructed.

    eg:
        {UP:<walk up animation>,
         DOWN:<walk down animation>,
         SWINGSWORD:<swing sword animation>}

    """
    def _build_animation_dictionary(self, animation_dictionary, display_time):
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
        
"""
Interface for character states.

Methods that vary depending on character state should be defined here, and implemented in each concrete state.
"""
class CharacterState(metaclass=ABCMeta):
    def __init__(self, character):
        self.character = character

    @abstractmethod
    def draw(self):
        pass

    # get a transparent surface the size of the character's image
    def _get_blank_surface(self):
        return pygame.Surface((self.character.width, self.character.height), pygame.SRCALPHA).convert_alpha()

"""
DEBUG STATE
"""
class OverworldDebugState(CharacterState):
    def __init__(self, character):
        super(self.__class__, self).__init__(character)
        self.collision_box = self._get_collision_box()
        self.collision_box_position = self._get_collision_box_position()

    """
    Set the image of the character, but with a transparent blue box denoting the character's position rect
    and a transparent red box denoting the collision rect.
    """
    def draw(self):
        temp = self._get_blank_surface()
        temp.fill(BLUE)
        temp.set_alpha(128)

        temp.blit(self.character.current_frame, (0,0))

        temp.blit(self.collision_box, self.collision_box_position)

        self.character.image = temp

    """
    Return a transparent red surface to represent the collision rect for the character

    :return: collision_box - pygame.Surface
    """
    def _get_collision_box(self):
        collision_box = pygame.Surface((self.character.collision_rect.width, self.character.collision_rect.height), pygame.SRCALPHA)
        collision_box.convert_alpha()
        collision_box.fill(RED)
        collision_box.set_alpha(128)

        return collision_box

    """
    Return the (x,y) coordinates of the topleft corner of the collision box.
    Position is relative to the temp surface that collision_box will be displayed on.

    :return: (x,y) - tuple of ints
    """
    def _get_collision_box_position(self):
        x = (self.character.width - self.character.collision_rect.width)/2
        y = self.character.height - self.character.collision_rect.height

        return (x, y)

"""
ANIMATED STATE
"""
class OverworldState(CharacterState):
    def __init__(self, character):
        super(self.__class__, self).__init__(character)

    """
    Set the image of the charcter to be the next frame in the current animation.
    """
    def draw(self):
        temp = self._get_blank_surface()
        temp.blit(self.character.current_frame, (0,0))
        self.character.image = temp

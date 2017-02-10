import pygame
import env.components.character as character
import eventparser as ep

from pygame.locals import *
from actions import *

def main():
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((600, 400))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Animation TEST")

    spritesheet = './tests/characters/sprites/male_sprite_model.png'
    anim_dict = {UP:[2, 1, 0, 2, 3, 4],
                     DOWN:[10, 9, 8, 10, 11, 12],
                     RIGHT:[16, 17, 18, 16, 21, 22],
                     LEFT:[24, 25, 26, 24, 29, 30]}

    char = character.OverworldCharacter(spritesheet, position=[200, 150], num_cols=8, num_rows=4, default_image=10, display_time=100, animation_dictionary=anim_dict)

    actions = []
    direction = LEFT
    char.animations[direction].play()

    while True:

        actions = ep.parse_keymap(pygame.key.get_pressed())
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        DISPLAYSURF.fill((100, 50, 50))
        char.animations[direction].blit(DISPLAYSURF, (300, 200))
        pygame.display.update()
        CLOCK.tick(30)

if __name__ == '__main__':
    main()

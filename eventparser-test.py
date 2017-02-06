import pygame
from pygame.locals import *
import eventparser as ep


def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("EventParser TEST")

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        actions = ep.parse_keymap(keys)
        if len(actions) > 0:
            print("\nActions: " + str(actions))
        CLOCK.tick(15)

if __name__ == "__main__":
    main()

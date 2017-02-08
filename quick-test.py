import pygame
from pygame.locals import *
import eventparser as ep
from tools.maploader import MapLoader
from tools.camera import ScrollingCamera
from actions import *

def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300), RESIZABLE)
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("TEST")
    
    maploader = MapLoader()
    
    current_map = maploader.load_map('tests/maps/map1.tmx')
    view = ScrollingCamera(current_map, screensize=(400,300))
    
    position = [200, 150]

    while True:
        view.draw(DISPLAYSURF, tuple(position))
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == VIDEORESIZE:
                view.set_screensize((event.w, event.h))
                #TODO: make this rescale the map instead of expanding display area
                DISPLAYSURF = pygame.display.set_mode((event.w, event.h), RESIZABLE)

        actions = ep.parse_keymap(keys)
        for action in actions:
            if action == UP:
                position[1] -= 10
            elif action == DOWN:
                position[1] += 10
            elif action == LEFT:
                position[0] -= 10
            elif action == RIGHT:
                position[0] += 10

        CLOCK.tick(30)

if __name__ == "__main__":
    main()

from actions import *
import pygame

def check_collision(rect1, rect2):
    if rect1.colliderect(rect2):
        return rect2
    else:
        return None

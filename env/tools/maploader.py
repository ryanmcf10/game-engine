import pygame
from pytmx.util_pygame import load_pygame
from env.components.map import *

"""
Load a .tmx formatted map and create a Map object
"""
def load_map_tmx(filename):
    assert filename.endswith('.tmx'), "Map file must be .tmx formatted."

    mapfile = load_pygame(filename)
    height = mapfile.height * mapfile.tileheight
    width = mapfile.width * mapfile.tilewidth
    num_rows = mapfile.height
    num_cols = mapfile.width

    return Map(width, height, num_rows, num_cols, mapfile, map_format='tmx')

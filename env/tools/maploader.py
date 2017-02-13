import pygame
from pytmx.util_pygame import load_pygame

class MapLoader(object):
    """
    MAPLOADER

    Used within the environment to load new maps.
    Must have complete path to mapfile in order to use load_map

    PARAMS:
    filename - name of last loaded map
    height - height of last loaded map in pixels
    width - width of last loaded map in pixels
    """
    def __init__(self, filename):
        self.load_map(filename)

    def __repr__(self):
        return "<MapLoader>\nFilename: {}\n{} x {}".format(self.filename, self.width, self.height)

    def load_map(self, filename):
        """
        Using PyTMX, load a .tmx formatted mapfile and return a TiledMap
        Update the parameters of the class

        :param: filename - must be .tmx
        :return: map - TiledMap
        """
        assert filename.endswith('.tmx'), "Map file must be .tmx formatted."
        self.filename = filename
        self.mapfile = load_pygame(filename)
        self.height = self.mapfile.height * self.mapfile.tileheight
        self.width = self.mapfile.width * self.mapfile.tilewidth
        self.blockers = self._build_blockers()

    def _build_blockers(self):
        """
        Read the metadata of the map file and produce a list of pygame.Rect objects to represent blockers on the map.

        Used to check for collisions.
        """
        blockers = []
        
        for object in self.mapfile.objects:
            properties = object.__dict__
            position = pygame.Rect(object.x, object.y, object.width, object.height)

            if properties['name'] == 'blocker':
                blockers.append(position)

        return blockers

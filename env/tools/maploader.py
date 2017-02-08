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
    def __init__(self):
        self.filename = None
        self.height = 0
        self.width = 0

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
        result = load_pygame(filename)
        self.height = result.height * result.tileheight
        self.width = result.width * result.tilewidth
        return result

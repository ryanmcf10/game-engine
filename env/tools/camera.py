import pyscroll
from abc import ABCMeta, abstractmethod

class Camera(metaclass=ABCMeta):
    """
    CAMERA

    Abstract base class to determine interface for camera tools

    =======
    METHODS
    =======
    draw(surface)
    update()
    """
    
    @abstractmethod
    def draw(self, surface):
        """
        Draw the current viewport onto the main surface

        :param: surface - surface to be drawn to
        """
        pass        

    @abstractmethod
    def _update(self):
        """
        Update the postion of all elements within the viewport.

        Called before drawing the frame.
        """
        pass

class MenuCamera(Camera):
    """
    MENU CAMERA

    Renders the view of dedicated menu environments.
    Static camera (ie does not scroll)
    Does not use any map data.
    """
    def draw(self, surface):
        pass

    def _update(self):
        pass
    
class ScrollingCamera(Camera):
    """
    SCROLLING CAMERA

    Renders the view of interior/exterior environments.
    Requires map data to render view.
    """
    def __init__(self, mapdata, screensize, player_layer=1):
        self.screensize = screensize
        self._renderer = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(mapdata), screensize)
        self.player_layer = player_layer

        #scroll --> main camera for the world environment
        self.scroller = pyscroll.group.PyscrollGroup(map_layer=self._renderer, default_layer=self.player_layer)

    def draw(self, surface, position):
        assert type(position) is list, "Position must be list"
        self._update(position)
        self.scroller.draw(surface)

    def _update(self, position):
        self.scroller.center(position)
    
    def set_screensize(self, new_size):
        assert type(new_size) is tuple, "Screensize must be a tuple" 
        self.screensize = new_size
        self._renderer.set_size(new_size)

    #TODO
    def scale(self, new_size):
        pass

    def add(self, surface):
        self.scroller.add(surface)

    def update(self):
        self.scroller.update()

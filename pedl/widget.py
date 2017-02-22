import math
from .choices import ColorChoice

class PedlObject:
    """
    Basic PEDL Class

    Parameters
    ----------
    name   : str , optional
        Alias of Widget

    x : int, optional
        Horizontal Position

    y : int, optional
        Vertical Position

    w : int, optional
        Width

    h : int, optional
        Height
    """
    _x = 0.
    _y = 0.
    _w = 0.
    _h = 0.
    def __init__(self, name=None, **kwargs):
        if not name:
            name = self.obj

        self.name = name
        #Set Dimensions
        for dimension in ('x','y','w','h'):
            if dimension in kwargs:
                setattr(self,
                        dimension,
                        kwargs[dimension])

        self._fill = None

    @property
    def x(self):
        """
        Starting position of the left side of the Widget
        """
        return self._x

    @x.setter
    def x(self, val):
        self._x = self._set_property(val, dtype=int)


    @property
    def y(self):
        """
        Starting position of the top of the widget
        """
        return self._y

    @y.setter
    def y(self, val):
        self._y = self._set_property(val, dtype=int)


    @property
    def w(self):
        """
        Width of the Widget
        """
        return self._w

    @w.setter
    def w(self, val):
        self._w = self._set_property(val, dtype=int)
    
    
    @property
    def h(self):
        """
        Height of the Widget
        """
        return self._h

    @h.setter
    def h(self, val):
        self._h = self._set_property(val, dtype=int)


    @property
    def center(self):
        """
        Position of the center of the widget
        """
        return (self.x+round(self.w/2), self.y + round(self.h/2))


    @property
    def bottom(self):
        """
        Position of the bottom of the widget
        """
        return self.y + self.h


    @property
    def right(self):
        """
        Right side of the widget
        """
        return self.x+ self.w


    def place_bottom(self, y):
        """
        Place the bottom of the widget at a certain height
        """
        self.y = y - self.h
        return self.y

    
    def place_right(self, x):
        """
        Place the bottom of the widget at a certain height
        """
        self.x = x - self.w
        return self.x


    def recenter(self, x=None, y=None):
        """
        Place the center of the widget at a x,y position
        """
        if x:
            self.x = x - round(self.w/2)
        if y:
            self.y = y - round(self.y/2)

        return self.x, self.y


    def _set_property(self, value, dtype=None):
            if dtype and not isinstance(value, dtype):
                value = dtype(value)

            return value


class Widget(PedlObject):
    """
    The basic Widget that all others inherit from, defining positioning and
    fill coloring settings

    Parameters
    ----------
    name   : str , optional
        Alias of Widget

    x : int, optional
        Horizontal Position

    y : int, optional
        Vertical Position

    w : int, optional
        Width

    h : int, optional
        Height
    
    Attributes
    ----------
    visibility : :class:`.Visibility`
        Visibility Settings for Widget
    """

    #Default Widget Info
    minor    = 1
    release  = 1
    template = 'widget.edl'
    obj      = None

    _fill    = None
    _colorPV = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Visibility Info
        self.visibility = Visibility()


    @property
    def vanishing(self):
        """
        Whether or not valid visibility information has been entered
        """
        return self.visibility.valid

    @property
    def colorPV(self):
        """
        Color PV to change fill based on different statuses
        """
        return self._colorPV

    @colorPV.setter
    def colorPV(self, value):
        self._colorPV = value


    @property
    def fill(self):
        """
        Background fill in the Widget, if set to None, the display background
        is used. Otherwise this should be a named color provided in the
        :class:`.ColorChoice` or if the color you want is unavailable an
        integer in ``(0,94)`` specifying the index of the desired color 
        """
        return self._fill


    @fill.setter
    def fill(self, value):
        if isinstance(value, NoneType):
            self._fill = value

        elif value in ColorChoice:
            self._fill = value

        elif value in range(0,94):
            self._fill = int(value)

        else:
            self._fill = ColorChoice(value)


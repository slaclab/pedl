import numpy as np
from .errors import DimensionError

class Widget:
    """
    Basic Widget Class

    Parameters
    ----------
    name   :

    parent :

    x : int
        Horizontal Position

    y : int
        Vertical Position

    w : int
        Width

    h : int
        Height
    """
    #Default Widget Info
    obj      = 'WidgetClass'
    minor    = 1
    release  = 1
    template = 'widget.edl'

    def __init__(name=None, **kwargs):

        #Environment Variables 
        if not name:
            name = self.obj

        self.name   = name

        #Set Dimensions
        for dimension in ('x','y','w','h'):
            if dimension in kwargs:
                setattr(self,
                        '_{}'.format(dimension),
                        kwargs[dimension])

        self._fill = None

    @property
    def x(self):
        """
        Starting position of the left side of the Widget
        """
        self._x

    @x.setter
    def x(self, val):
        self._x = self._set_property(val, dtype=int)


    @property
    def y(self):
        """
        Starting position of the top of the widget
        """
        self._y

    @y.setter
    def y(self, val):
        self._y = self._set_property(val, dtype=int)


    @property
    def w(self):
        """
        Width of the Widget
        """
        self._w

    @w.setter
    def w(self, val):
        self._w = self._set_property(val, dtype=int)
    
    
    @property
    def h(self):
        """
        Height of the Widget
        """
        self._h

    @w.setter
    def h(self, val):
        self._h = self._set_property(val, dtype=int)


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


    @property
    def center(self):
        """
        Position of the center of the widget
        """
        return (self.x+self.w/2, self.y + self.h/2)


    def place_bottom(self, y):
        """
        Place the bottom of the widget at a  certain height
        """
        self.y = y - self.h
        return self.y

    
    def place_right(self, x):
        """
        Place the bottom of the widget at a  certain height
        """
        self.x = x - self.w
        return self.x


    @property
    def _fill_index(self):
        """
        Formatted index call for EDL file
        """
        if not self._fill:
            return False

        elif isinstance(self._fill, ColorChoice):
            return self._fill.value

        else:
            return self._fill

    def _set_property(self, value, dtype=None):
            if dtype and not isinstance(value, dtype):
                value = dtype(value)

            return value

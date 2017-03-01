from ..widget  import Widget
from ..choices import ColorChoice 

class Shape(Widget):
    """
    Basic Shape Widget

    Many of the basic widgets in EDM have these simple properties
    """
    template   = 'shape.edl'
    _linewidth = 1
    _fill      = None
    _lineColor = ColorChoice.Black

    @property
    def lineWidth(self):
        """
        Width of the frame around the Widget
        """
        return self._linewidth

    @lineWidth.setter
    def lineWidth(self, value):
        self._linewidth = int(value) 

    @property
    def lineColor(self):
        """
        Color of the frame around the Widget
        """
        return self._lineColor

    @lineColor.setter
    def lineColor(self, value):
        self._lineColor = ColorChoice(value)
    
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
        if value is None:
            self._fill = value

        else:
            self._fill = ColorChoice(value)



class Circle(Shape):
    widgetClass = 'activeCircleClass'
    minor   = 0
    release = 0


class Rectangle(Shape):
    widgetClass = 'activeRectangleClass'
    minor   = 0
    release = 0


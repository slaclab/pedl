from .widget  import Widget
from .choices import ColorChoice 

class Shape(Widget):

    _linewidth = 1
    _lineColor = ColorChoice.Black

    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, value):
        return self._linewidth = self.set_property(value, dtype=int)

    @property
    def lineColor(self):
        return self._lineColor

    @lineColor.setter(self, value):
        return self._lineColor = self.set_property(value, dtype=ColorChoice)


class Circle(Shape):
    widgetClass = 'activeCircleClass'
    minor   = 0
    release = 0


class Rectangle(Shape):
    widgetClass = 'activeRectangleClass'
    minor   = 0
    release = 0


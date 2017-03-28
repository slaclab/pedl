"""
EDM is capable of drawing a few basic shapes, :class:`.Rectangle` and
:class:`.Circle`. Because both have identical options, just with a different
drawing command, we have a shared :class:`.Shape` object that each inherits
"""
from ..widget  import Widget
from ..choices import ColorChoice 
from ..utils   import pedlproperty

class Shape(Widget):
    """
    Basic Shape Widget
    """
    template   = 'shape.edl'
    linewidth = pedlproperty(int, default=1, doc='Stroke of surrounding border')
    fill      = pedlproperty(ColorChoice, doc='Background fill in the widget')
    lineColor = pedlproperty(ColorChoice, default=ColorChoice.Black,
                             doc='Color of surrounding Widget frame')

class Circle(Shape):
    widgetClass = 'activeCircleClass'
    minor   = 0
    release = 0


class Rectangle(Shape):
    widgetClass = 'activeRectangleClass'
    minor   = 0
    release = 0


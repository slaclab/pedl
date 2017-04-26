"""
EDM is capable of drawing a few basic shapes, :class:`.Rectangle` and
:class:`.Circle`. Because both have identical options, just with a different
drawing command, we have a shared :class:`.Shape` object that each inherits
"""
####################
# Standard Library #
####################
from copy import copy
####################
#    Third Party   #
####################

####################
#     Package      #
####################
from ..widget  import Widget
from ..choices import ColorChoice 
from ..utils   import pedlproperty

class Shape(Widget):
    """
    Basic Shape Widget
    """
    template   = 'shape.edl'
    lineWidth = pedlproperty(int, default=1, doc='Stroke of surrounding border')
    fill      = pedlproperty(ColorChoice, doc='Background fill in the widget')
    lineColor = pedlproperty(ColorChoice, default=ColorChoice.Black,
                             doc='Color of surrounding Widget frame')
    alarm  = pedlproperty(bool, default=False,
                          doc='Fill color will be sensitive to the '
                              'alarm state of the PV')


class Lines(Shape):
    """
    """
    widgetClass = 'activeLineClass'
    template    = 'lines.edl'
    minor       = 0
    release     = 1
    
    points = pedlproperty(list, default=list(),
                          doc="List of (x,y) points to draw line")

    @property
    def x(self):
        """
        Horizontal position
        """
        if not self.points:
            return 0

        return min([p[0] for p in self.points])


    @property
    def y(self):
        """
        Vertical Position
        """
        if not self.points:
            return 0

        return min([p[1] for p in self.points])


    @x.setter
    def x(self, x):
        if self.points:
            shift = x - self.x
            self.points = [(p[0]+shift, p[1]) for p in self.points] 


    @y.setter
    def y(self, y):
        if self.points:
            shift = y - self.y
            self.points = [(p[0], p[1]+shift) for p in self.points] 

    
    @property
    def w(self):
        """
        Width of shape
        """
        if not self.points:
            return 0

        positions = [p[0] for p in self.points]
        return max(positions) - min(positions)



    @property
    def h(self):
        """
        Height of shape
        """
        if not self.points:
            return 0

        positions = [p[1] for p in self.points]
        return max(positions) - min(positions)


    @w.setter
    def w(self, w):
        if self.points:
            #Keep track of starting position
            x = self.x
            #Scale widgets
            scale     = w / self.w
            self.points = [(round(p[0]*scale), p[1]) for p in self.points]
            #Reset widget to starting position
            self.x = x


    @h.setter
    def h(self, h):
        if self.points:
            #Keep track of starting position
            y = self.y
            #Scale widgets
            scale = h / self.h
            self.points = [(p[0], round(p[1]*scale)) for p in self.points]
            #Reset widget to starting position
            self.y = y


    @property
    def numPoints(self):
        """
        Number of points along line
        """
        return len(self.points)


class GateValve(Lines):
    points = copy(Lines.points)
    points.default = [(0,0),(4,2),(4,0),(0,2),(0,0)]

class Stopper(Lines):
    points = copy(Lines.points)
    points.default = [(0,2),(2,0),(7,0),(9,2),
                      (9,7),(7,9),(2,9),(0,7)]

class Camera(Lines): 
    points = copy(Lines.points)
    points.default = [(0,0),(4,0),(2,2),(4,2),
                      (4,6),(0,6),(0,2),(2,2)]

class Circle(Shape):
    widgetClass = 'activeCircleClass'
    minor   = 0
    release = 0


class Rectangle(Shape):
    widgetClass = 'activeRectangleClass'
    minor   = 0
    release = 0


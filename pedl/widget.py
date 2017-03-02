from .utils   import Visibility
from .choices import ColorChoice
from .errors  import DesignerError

class PedlObject:
    """
    Basic PEDL Class

    Parameters
    ----------
    name   : str , optional
        Alias of Widget

    parent : ``PedlObject``, optional
        Parent of object

    x : int, optional
        Horizontal Position

    y : int, optional
        Vertical Position

    w : int, optional
        Width

    h : int, optional
        Height
    """
    widgetClass = None
    _x   = 0
    _y   = 0
    _w   = 0
    _h   = 0

    def __init__(self, name=None, parent=None, **kwargs):
        if not name:
            name = self.widgetClass

        self.name   = name
        self.parent = parent

        #Set Dimensions
        for dimension in ('x','y','w','h'):
            if dimension in kwargs:
                setattr(self,
                        dimension,
                        kwargs[dimension])


    @property
    def x(self):
        """
        Starting position of the left side of the Widget
        """
        return self._x

    @x.setter
    def x(self, val):
        self._x = int(val)


    @property
    def y(self):
        """
        Starting position of the top of the widget
        """
        return self._y

    @y.setter
    def y(self, val):
        self._y = int(val)


    @property
    def w(self):
        """
        Width of the Widget
        """
        return self._w

    @w.setter
    def w(self, val):
        self._w = int(val)
    
    
    @property
    def h(self):
        """
        Height of the Widget
        """
        return self._h

    @h.setter
    def h(self, val):
        self._h = int(val)


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
            self.y = y - round(self.h/2)

        return self.x, self.y


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


class Screen(PedlObject):
    """
    Control over EDM Screen Parameters
    
    Attributes
    ----------
    margin : int
        Margin sizes for the screen
    """
    template    = 'window.edl'
    minor       = 0
    release     = 1
    margin      = 5

    #Default Settings
    _background = ColorChoice.Grey
    _foreground = ColorChoice.Black
    _w = 750
    _h = 1100

    @property
    def background(self):
        """
        Background color of EDM screen as a :class:`.ColorChoice`
        """
        return self._background

    @background.setter
    def background(self, color):
        self._background = ColorChoice(color)

    @property
    def foreground(self):
        """
        Foreground color of EDM screen as a :class:`.ColorChoice`
        """
        return self._foreground

    @foreground.setter
    def foreground(self, color):
        self._foreground = ColorChoice(color)


    def setLayout(self, layout, resize=False, origin=None):
        """
        Set the main layout

        This clears the current screen and draws all of the widgets as
        described by the given layout. By default, the layout is centered in
        the horizontal and placed at the top margin in the vertical.

        Parameters
        ----------
        layout : :class:`.pedl.Layout`
            Master layout for screen

        resize : bool , optional
            Resize the screen to fit the given Layout. In this case the layout
            will be placed in the upper left hand corner, seperated from the
            edge of the screen by the :attr:`.margin` 

        origin : tuple, optional
            (x,y) location for the top left corner of the layout
        
        Raises
        ------
        DesignerError:
            The screen must belong to a parent :class:`.Designer`
        """
        if not self.parent:
            raise DesignerError("Screen must have a designer parent"
                                " to set the layout")
        if not layout.widgets:
            raise ValueError("Provided layout has not Widgets!")

        #Resize screen
        if resize:
            logger.debug("Resizing screen to fit layout ...")
            origin = (self.margin, self.margin)
            self.w = layout.w + 2*self.margin
            self.h = layout.h + 2*self.margin

        #Move layout
        if origin:
            layout.x, layout.y = origin
        #If no origin, use top and center
        else:
            layout.y = self.margin
            layout.recenter(x=self.center[0])

        #Check screen size
        if layout.right  > self.right or layout.bottom > self.h:
            logger.warning("Layout exceeds the boundary of the screen")

        self.parent.widgets = [layout]

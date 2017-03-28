from .utils   import pedlproperty, Visibility
from .choices import ColorChoice
from .errors  import DesignerError

from copy import copy
import six
class PedlMeta(type):

    def __new__(cls, name, bases, clsdict):
        #Create new PedlObject
        clsobj = super().__new__(cls, name, bases, clsdict)
        #Storage for pedlproperty info
        clsobj._pedl      = dict()

        #Find all child properties
        for base in reversed(bases):

            if not hasattr(base, '_pedl'):
                continue

            for attr, prop in base._pedl.items():
                clsobj._pedl[attr] = prop

        #Find all pedlproperties
        for attr, value in clsdict.items():
            if isinstance(value, pedlproperty):
                #Store record of pedl properities
                clsobj._pedl[attr] = value

        #Notify property of the attribute name
        for attr, prop in clsobj._pedl.items():
            prop.attr = attr

        return clsobj


class PedlObject(six.with_metaclass(PedlMeta, object)):
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
    
    w = pedlproperty(int, default=0, doc='Width  of the widget')
    h = pedlproperty(int, default=0, doc='Height of the widget')
    x = pedlproperty(int, default=0, doc='Horizontal position of the widget')
    y = pedlproperty(int, default=0, doc='Vertical position of the widget')

    def __init__(self, name=None, parent=None, **kwargs):
        if not name:
            name = self.widgetClass

        self.name       = name
        self.parent     = parent

        #Store default value within the class
        self.attributes = dict((prop.attr, prop.default) for prop in
                                self._pedl.values())

        #Update kwargs 
        for key, val in kwargs.items():
            try:
                setattr(self, key, val)

            except AttributeError as e:
#                raise TypeError('Got unexpected keyword {}'.format(key))
                print("Sending to next level {}".format(e))
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

    colorPV = pedlproperty(str, doc="PV to control widget color")
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


class Screen(PedlObject):
    """
    Control over EDM Screen Parameters

    Attributes
    ----------
    margin : int
        Margin sizes for the screen
    """
    #Template properties
    template    = 'window.edl'
    minor       = 0
    release     = 1
    margin      = 5

    #PEDL properties
    background = pedlproperty(ColorChoice, default=ColorChoice.Grey,
                              doc='Background color of the EDM screen ' 
                                   'as a :class:`.ColorChoice')
    foreground = pedlproperty(ColorChoice, default=ColorChoice.Black,
                              doc='Foreground color of the EDM screen ' 
                                   'as a :class:`.ColorChoice')

    #Change default settings
    w = copy(PedlObject.w)
    h = copy(PedlObject.h)
    w.default = 750
    h.default = 1100

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

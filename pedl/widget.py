####################
# Standard Library #
####################
import logging
from copy import copy

####################
#    Third Party   #
####################
import six

####################
#     Package      #
####################
from .utils   import pedlproperty, Visibility
from .choices import ColorChoice
from .errors  import DesignerError


logger = logging.getLogger(__name__)

class PedlMeta(type):
    """
    Metaclass for PedlObject
    """
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

    The generic class for any object that is rendered by pedl. 
    
    Parameters
    ----------
    name   : str , optional
        Alias of Widget

    parent : ``PedlObject``, optional
        Parent of object

    attributes : dict
        All properties that are directly interepreted by a pedl template
    """
    widgetClass = None
    
    w = pedlproperty(int, default=0, doc='Width of the widget')
    h = pedlproperty(int, default=0, doc='Height of the widget')
    x = pedlproperty(int, default=0, doc='Horizontal position of the widget')
    y = pedlproperty(int, default=0, doc='Vertical position of the widget')

    def __init__(self, name=None, parent=None, **kwargs):
        self.name       = name or self.widgetClass
        self.parent     = parent

        #Store default value within the class
        self.attributes = dict((prop.attr, copy(prop.default)) for prop in
                                self._pedl.values())

        #Update kwargs 
        for key, val in kwargs.items():
            try:
                setattr(self, key, val)

            except AttributeError as e:
                logger.debug('Found keyword {} not associated with '
                             '{} attribute'.format(e, self.__class__))
                                                   

    @property
    def properties(self):
        """
        All pedlproperties
        """
        return list(self._pedl.keys())


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


    def placeBottom(self, y):
        """
        Place the bottom of the widget at a certain height
        """
        self.y = y - self.h
        return self.y

    
    def placeRight(self, x):
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

    def __copy__(self):
        return self.__class__(**self.attributes)


class Widget(PedlObject):
    """
    The basic Pedl Widget

    Every widget is a rectangular box that can be modifed and moved freely or
    placed within a layout object. While the widget does not correspond to
    directly to an EDM widget, it provides the base functionality to manipulate
    the displayed object in space. Actual display information is left to
    subclasses. 

    Besides spatial attributes, the base Widget class also contains the colorPV
    and visibility attributes. These are present because they are common to all
    widgets in EDM,  :attr:`.Widget.visibility` controls the settings for the
    visibility PV and associated display range, and :attr:`.alarmPv` allows the
    widget to display changes of state as specific alarm colors

    Attributes
    ----------
    name   : str , optional
        Alias of Widget
    """
    #Default Widget Info
    minor    = 1
    release  = 1
    template = 'widget.edl'

    alarmPV     = pedlproperty(str, doc="PV to monitor alarm state")
    visibility  = pedlproperty(Visibility.is_visibility,
                               default=Visibility(),
                               doc='Visibility Settings for Widget')

    def setGeometry(self, x, y, w, h):
        """
        Set the geometry of the widget

        Parameters
        ----------
        x : int
            Left position of widget

        y : int
            Top position of widget

        w : int
            Width of widget

        h : int
            Height of widget
        """
        self.x, self.y, self.w, self.h = x, y, w, h


    @property
    def vanishing(self):
        """
        Whether or not valid visibility information has been entered
        """
        return self.visibility.valid


class MainWindow(PedlObject):
    """
    Basic EDM Screen

    The EDM screen is represented as a PEDL object in order to control the size
    and background color of the display. This is one area where PEDL diverges
    from Qt, as EDM neccesitates a screen to display any widgets.

    A default window is automatically instantiated inside the Designer as
    :attr:`.window`. This can be tweaked to have the desired EDM output.
    Finally, if you are using layouts, use :meth:`.setLayout` with resize set
    to ``True``. This will abstract away the concern for resizing the screen,
    and simply set the window size based on the provided layout.

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
                                   'as a :class:`.ColorChoice`')
    foreground = pedlproperty(ColorChoice, default=ColorChoice.Black,
                              doc='Foreground color of the EDM screen ' 
                                   'as a :class:`.ColorChoice`')

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

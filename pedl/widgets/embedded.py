"""
EmbeddedWindow Widget
"""
############
# Standard #
############
import os
import logging

###############
# Third Party #
###############
import six

##########
# Module #
##########
from ..widget  import Widget
from ..utils   import LocalPv, find_screen_size, pedlproperty

logger = logging.getLogger(__name__)

class Display(object):
    """
    Data structure to represent Embedded Display
    """
    def __init__(self, name, path, macros):
        self.name   = name
        self.path   = path
        self.macros = macros
    
    @classmethod
    def from_edl(cls, edl):
        """
        Form a generic Display from an EDL file
        """
        #Find filename
        name, ext = os.path.splitext(os.path.basename(edl))

        #Check extension is .edl
        if not ext == '.edl':
            raise ValueError('Must be an EDL file, not {}'
                             ''.format(ext))

        return cls(name, edl, None)


class EmbeddedWindow(Widget):
    """
    Embedded Window

    Basic widget to display other EDM files. Within EDM, the EmbeddedWindow has
    a few different implementations, PEDL only instantiates the Menu version.
    In this setup, a single PV controls which of the displays is shown.

    For the most common use case where you only have a single display, the
    widget sets a few defaults for conveinence. By using a local PV, window is
    set to automatically use the first display provided. There is also an
    ``autoscale`` feature that parses the width and height of displays that you
    add to the EmbeddedWindow. This is obviously useful if you would like to
    remain oblivious to the exact dimensions of the embedded edl file, but it
    does require that the path to the display exists.

    Parameters
    ----------
    autoscale: bool
        Whether to scale the widget to largest dimensions of embedded displays 
    """
    widgetClass = 'activePipClass'
    major       = 4
    minor       = 1
    release     = 0
    template    = 'embedded.edl'

    #Custom Properties
    controlPv = pedlproperty(str, default=LocalPv('emb-window', 0),
                             doc="PV to control embedded window")
    displays  = pedlproperty(list, default =[],
                             doc="List of displays inside EmbeddedWindow")

    def __init__(self, autoscale=True,  **kwargs):
        self.autoscale = autoscale

        #Widget initialize
        super(EmbeddedWindow, self).__init__(**kwargs)

        #Replace strings with proper Display datatypes
        self.displays = [d if isinstance(d, Display)
                           else Display.from_edl(d)
                           for d in self.displays]
        #Fit to current displays 
        if self.autoscale:
            self.resize()


    @property
    def count(self):
        """
        Number of displays
        """
        return len(self.displays)


    def insertDisplay(self, index, display):
        """
        Insert a display into the EmbeddedWindow

        Parameters
        ----------
        index : int
            Index in stack to place display
        
        display : str or :class:`.Display`
            String of filepath or complete Display object
        """
        if isinstance(display, six.string_types):
            display = Display.from_edl(display)

        elif not isinstance(display, Display):
            raise ValueError("{} is not a valid display"
                             "".format(display))

        self.displays.insert(index, display)

        if self.autoscale:
            self.resize()


    def addDisplay(self, display):
        """
        Add a display onto the EmbeddedWindow

        Parameters
        ----------
        display : str or :class:`.Display`
            String of filepath or complete Display object
        """
        self.insertDisplay(self.count, display)


    def resize(self):
        """
        Resize the widget to fully fit each embedded display

        Requires that all embedded displays have their file path readable so
        that the width and height of each can be parsed.

        Returns
        -------
        dimension : tuple
            New width and height of EmbeddedWindow
        """
        if not self.displays:
            return 

        dimensions = [find_screen_size(open(d.path, 'r'))
                      for d in self.displays]
        self.w = max(dimensions, key= lambda d : d[0])[0] 
        self.h = max(dimensions, key= lambda d : d[1])[1] 
        return self.w, self.h 

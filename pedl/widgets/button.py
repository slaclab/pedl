"""
Support for the variety of buttons contained within EDM
"""
############
# Standard #
############
import copy
import logging
from collections import namedtuple
###############
# Third Party #
###############
import six

##########
# Module #
##########
from .shape    import Shape
from ..utils   import Font, pedlproperty
from ..layout  import Layout, StackedLayout
from ..choices import ColorChoice, FontChoice
from .embedded import Display
logger = logging.getLogger(__name__)


class Button(Shape):

    #PEDL properties
    controlPv = pedlproperty(str, doc='Name of the Pv to control')
    fontColor = pedlproperty(ColorChoice, default=ColorChoice.Black,
                             doc='Color of the font inside the button')
    font      = pedlproperty(Font.is_font, default = Font(),
                             doc= 'Font as indicated by :class:`.Font`')
    
    
    #Change defaults
    fill = copy.copy(Shape.fill)
    fill.default = ColorChoice.Grey

    lineColor = copy.copy(Shape.lineColor)
    lineColor.default = None


    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        #Make border disappear if set to None
        if not self.lineColor:
            self.lineColor = self.fill
    
    @property
    def lineWidth(self):
        raise NotImplementedError("Button frame can only be modifed "
                                  "using lineColor attribute.")
   

    def blend(self, color=ColorChoice.Grey):
        """
        Make the MenButton all one uniform color
        """
        self.lineColor = ColorChoice(color)
        self.fill      = ColorChoice(color)
        self.fontColor = ColorChoice(color)


    @classmethod
    def buttonize(cls, obj, blend=ColorChoice.Grey, **kwargs):
        """
        Create a :class:`.StackedLayout` that turns an existing widget into a
        button

        For most cases a new :class:`.StackedLayout` is created with a button
        placed at the bottom. However, if the object given to buttonize is
        already a :class:`.StackedLayout` the button is simply placed on the
        bottom and returned.

        Parameters
        ----------
        obj : :class:`.Widget` or :class:`.Layout`
            Layout or Widget to create transform into a button

        blend : :class:`.ColorChoice`
            Make MenuButton monocolor to match a background. Set to None, to
            use default Widget coloring

        kwargs :
            Define additional button specific keyword arguments. These can not
            include any parameter involving the geometry

        Returns
        -------
        :class:`.StackedLayout`
            StackedLayout with a button behind it of matching geometry
        """
        #Create Button
        button = cls(x=obj.x,y=obj.y, w=obj.w, h=obj.h, **kwargs)

        #Color MenuButton
        if blend:
            button.blend(blend)

        #Add to existing stacked layout
        if isinstance(obj, StackedLayout):
            obj.insertWidget(0, button)
            return obj

        else:
            #Create Layout
            l = StackedLayout()

            #Add Widgets
            l.addWidget(button)

            if isinstance(obj, Layout):
                l.addLayout(obj)
            else:
                l.addWidget(obj)

        return l
        #Create layout
        l = super().buttonize(obj, invisible=False, **kwargs)





class MessageButton(Button):
    """
    MessageButton Widget

    The simplest Pv interaction widget, MessageButton sends a single Pv a
    single value when pressed. The Widget will need a value and controlPv to
    function properly within EDM
    """
    #Templating information
    widgetClass = 'activeMessageButtonClass' 
    minor       = 1
    release     = 0
    template    = 'message.edl'

    #Defaults
    label     = pedlproperty(str,  default='', doc='Label of Button')
    value     = pedlproperty(None, default='', doc='Value to apply to controlPv')
    invisible = pedlproperty(int, default=False,
                             doc='The visibility of the button, if set to '
                                 'True, the button will still be clickable, '
                                 'but will not be seen by the user until '
                                 'moused over')
    
    @classmethod
    def buttonize(cls, obj, invisible=True, **kwargs):
        """
        Create a :class:`.StackedLayout` that turns an existing widget into a
        button

        For most cases a new :class:`.StackedLayout` is created with a button
        placed at the bottom. However, if the object given to buttonize is
        already a :class:`.StackedLayout` the button is simply placed on the
        bottom and returned.

        Parameters
        ----------
        obj : :class:`.Widget` or :class:`.Layout`
            Layout or Widget to create transform into a button

        invisible : bool, optional
            Whether to hide the button or not

        kwargs : 
            Define additional button specific keyword arguments. These can not
            include any parameter involving the geometry or visibility

        Returns
        -------
        :class:`.StackedLayout`
            StackedLayout with an button behind it of matching geometry
        """
        #Create layout
        l = super().buttonize(obj, blend=None, **kwargs)
        
        if invisible:
            l.widgets[0].invisible = True

        return l


class MenuButton(Button):
    """
    MenuButton Widget

    This widget offers control over any Enum Pv with a dropdown menu

    Parameters
    ----------
    control : str
        The Enum Pv to associate with the menu button
    """
    #Templating information
    widgetClass = 'activeMenuButtonClass'
    major    = 4
    minor    = 0
    release  = 0
    template = 'menu.edl'


class RelatedDisplay(Button):
    """
    DisplayButton Widget

    Launches an external EDL file in a separate window
    """
    widgetClass = 'relatedDisplayClass'
    major    = 4
    minor    = 4
    release  = 0
    template = 'display.edl'

    displays = pedlproperty(list, default=[],
                            doc='List of external displays')
        
    def __init__(self, *args, **kwargs):
        super(RelatedDisplay, self).__init__(*args, **kwargs)
        self.displays = [d if isinstance(d, Display)
                           else Display.from_edl(d)
                           for d in self.displays]


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


    def addDisplay(self, display):
        """
        Add another Display into the RelatedDisplay list

        Parameters
        ----------
        display : str or :class:`.Display`
            String of filepath or complete Display object
        """
        self.insertDisplay(self.numDisplays, display)


    @property
    def numDisplays(self):
        """
        Number of displays
        """
        return len(self.displays)


Command = namedtuple('Command', ['name', 'command'])

class ShellCommand(Button):
    """
    ShellCommand Widget

    Runs a given shell command
    """
    widgetClass = 'shellCmdClass'
    major    = 4
    minor    = 3
    release  = 0
    template = 'shell.edl'
   
    commands = pedlproperty(list, default=[],
                            doc='List of Commands to make available')

    def insertCommand(self, index, cmd):
        """
        Insert a command into the ShellCommand queue

        Parameters
        ----------
        index : int
            Index in stack to place command
        
        cmd : :class:`.Command`
            Command to add to button 
        """
        if isinstance(cmd, tuple):
            cmd = Command(*cmd)

        self.commands.insert(index, cmd)


    def addCommand(self, cmd):
        """
        Add another Command into the ShellCommand list

        Parameters
        ----------
        cmd : :class:`.Command`
            Command to add to button 
        """
        self.insertCommand(self.numCommands, cmd)


    @property
    def numCommands(self):
        """
        Number of commands
        """
        return len(self.commands)

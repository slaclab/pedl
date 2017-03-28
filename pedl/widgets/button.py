"""
Support for the variety of buttons contained within EDM
"""
############
# Standard #
############
import copy
import logging

###############
# Third Party #
###############


##########
# Module #
##########
from .shape    import Shape
from ..utils   import Font, pedlproperty
from ..layout  import StackLayout
from ..choices import ColorChoice, FontChoice

logger = logging.getLogger(__name__)


class Button(Shape):

    #PEDL properties
    fontColor = pedlproperty(int, default=ColorChoice.Black,
                             doc='Color of the font inside the button')
    invisible = pedlproperty(int, default=False,
                             doc='The visibility of the button, if set to '
                                 'True, the button will still be clickable, '
                                 'but will not be seen by the user until '
                                 'moused over')
    fill      = pedlproperty(ColorChoice, default=ColorChoice.Grey,
                             doc= 'Fill color of the Widget')
    lineColor = pedlproperty(ColorChoice,
                             doc= 'Color of the border surrounding the button')

    #Font Choice
    _font = Font(font=FontChoice.Helvetica, size=18)

    def __init__(self, control=None, **kwargs):
        self.control = control
        super().__init__(**kwargs)

        #Make border disappear if set to None
        if not self.lineColor:
            self.lineColor = self.fill

    @property
    def font(self):
        """
        Button Font as indicated by :class:`.Font`
        """
        return self._font

    @font.setter
    def font(self, font):
        if not isinstance(font, Font):
            raise TypeError("Must be a Font object")

        self._font = font

    @property
    def lineWidth(self):
        raise NotImplementedError("Button frame can only be modifed "
                                  "using lineColor attribute.")

    @classmethod
    def buttonize(cls, obj, invisible=True, **kwargs):
        """
        Create a :class:`.StackLayout` that turns an existing widget into a
        button

        Parameters
        ----------
        obj : :class:`.Widget` or :class:`.Layout`
            Layout or Widget to create transform into a button

        invisible : bool, optional
            Whether to hide the button or not

        kwargs : 
            Define additional button specific keyword arguments. These can not
            include any parameter involving the geometry

        Returns
        -------
        :class:`.StackLayout`
            StackLayout with an button behind it of matching geometry
        """
        #Create Button
        button = cls(x=obj.x,y=obj.y, w=obj.w, h=obj.h, **kwargs)
        if invisible:
            button.invisible = True

        #Create Layout
        l = StackLayout()

        #Add Widgets
        l.addWidget(button)
        if isinstance(obj, Layout):
            l.addLayout(obj)
        else:
            l.addWidget(obj)

        return l


class MessageButton(Button):
    """
    MessageButton Widget

    The simplest PV interaction widget, MessageButton sends a single PV a
    single value when pressed. The Widget will need a value and controlPV to
    function properly within EDM

    Parameters
    ----------
    value : str, int, float
        Desired value associated with a press of the button

    control : str
        PV to send ``value``

    label : str
        Optional Label to place on the button when visible
    """
    #Templating information
    widgetClass = 'activeMessageButtonClass' 
    minor       = 1
    release     = 0
    template    = 'message.edl'

    #Defaults
    label = pedlproperty(str, default='', doc='Label of Button')

    def __init__(self, value=None, label=None, **kwargs):
        super().__init__(**kwargs)
        self.value   = value
        self.label   = label


class MenuButton(Button):
    """
    MenuButton Widget

    This widget offers control over any Enum PV with a dropdown menu

    Parameters
    ----------
    control : str
        The Enum PV to associate with the menu button
    """
    #Templating information
    widgetClass = 'activeMenuButtonClass'
    major    = 4
    minor    = 0
    release  = 0
    template = 'button.edl'

    invisible = copy.copy(Button.invisible)

    @invisible.setter
    def invisible(self, val):
        if val:
            raise ValueError('MenuButton can not be made invisible, '
                             'use the blend method to make it match '
                             'the screen background')
        else:
            self.val = int(val)

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
        Create a :class:`.StackLayout` that turns an existing widget into a
        button

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
        :class:`.StackLayout`
            StackLayout with a button behind it of matching geometry
        """
        #Create layout
        l = super().buttonize(obj, invisible=False, **kwargs)

        #Color MenuButton
        if blend:
            l.widgets[0].blend(blend)

        return l

"""
Support for the variety of buttons contained within EDM
"""
############
# Standard #
############
import logging

###############
# Third Party #
###############


##########
# Module #
##########
from .shape    import Shape
from ..choices import ColorChoice, FontChoice
from ..font    import Font
from ..layout  import StackLayout

logger = logging.getLogger(__name__)


class Button(Shape):
    
    #Defaults
    _fontColor = ColorChoice.Black
    _font      = Font(font=FontChoice.Helvetica, size=18)
    _invisible = False
    _fill      = ColorChoice.Grey
    _lineColor = None

    def __init__(self, control=None, **kwargs):
        self.control = control
        super().__init__(**kwargs)

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
    def fontColor(self):
        """
        Color of the font inside the button
        """
        return self._fontColor

    @fontColor.setter
    def fontColor(self, font):
        self._fontColor = ColorChoice(font)

    @property
    def lineWidth(self):
        raise NotImplementedError("Button frame can only be modifed "
                                  "using lineColor attribute.")


    @property
    def lineColor(self):
        """
        Color of the border surrounding the button
       
        If set to None, the border surrounding the button will be non-existant
        """
        if not self._lineColor:
            return self.fill

        return self._lineColor

    @lineColor.setter
    def lineColor(self, color):
        if color:
            self._lineColor = ColorChoice(color)
        else:
            self._lineColor = None


    #Reimplementation so fill can not be None
    @property
    def fill(self):
        """
        Fill color of the Widget
        """
        return self._fill

    @fill.setter
    def fill(self, color):
        self._fill = ColorChoice(color)


    @property
    def invisible(self):
        """
        The visibility of the button, if set to True, the button will still be
        clickable, but won't be seen by the user until moused over
        """
        return self._invisible


    @invisible.setter
    def invisible(self, value):
        self._invisible = int(value)


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
    _label     = None

    def __init__(self, value=None, label=None, **kwargs):
        super().__init__(**kwargs)
        self.value   = value
        self.label   = label


    @property
    def label(self):
        """
        Label for the face of the button. If set to None, the button will be
        blank
        """
        return self._label

    @label.setter
    def label(self, value):
        if not value:
            self._label = ''
        else:
            self._label = value


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
    
    #Defaults
    _invisible = False

    @property
    def invisible(self):
        return self._invisible

    @invisible.setter
    def invisible(self, val):
        raise NotImplementedError('MenuButton can not be made invisible, '
                                  'use the blend method to make it match '
                                  'the screen background')


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

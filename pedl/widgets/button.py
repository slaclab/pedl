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
from ..layout  import Layout, StackedLayout
from ..choices import ColorChoice, FontChoice

logger = logging.getLogger(__name__)


class Button(Shape):

    #PEDL properties
    controlPv = pedlproperty(str, doc='Name of the Pv to control')
    fontColor = pedlproperty(ColorChoice, default=ColorChoice.Black,
                             doc='Color of the font inside the button')
    font      = pedlproperty(Font.is_font, default = Font(),
                             doc= 'Font as indicated by :class:`.Font`')
    invisible = pedlproperty(int, default=False,
                             doc='The visibility of the button, if set to '
                                 'True, the button will still be clickable, '
                                 'but will not be seen by the user until '
                                 'moused over')
    
    
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
        #Create Button
        button = cls(x=obj.x,y=obj.y, w=obj.w, h=obj.h, **kwargs)
        if invisible:
            button.invisible = True

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
    label = pedlproperty(str,  default='', doc='Label of Button')
    value = pedlproperty(None, default='', doc='Value to apply to controlPv')


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
        #Create layout
        l = super().buttonize(obj, invisible=False, **kwargs)

        #Color MenuButton
        if blend:
            l.widgets[0].blend(blend)

        return l

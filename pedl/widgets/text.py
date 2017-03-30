"""
Static Text Widget
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
from ..widget  import Widget
from ..utils   import pedlproperty, Font
from ..choices import AlignmentChoice, FontChoice, ColorChoice

logger = logging.getLogger(__name__)

class StaticText(Widget):
    """
    Basic Label Widget
    
    The counterpart to the QLabel Widget, this represents just a basic text
    entry. The implementatation in EDM has a few quirks, one of which being
    the color of the frame has to match the color of the font. EDM also uses
    an autoscale feature that is disabled in PEDL, this is largely because PEDL
    depends on knowing the exact size of different widgets to organize them
    into aligned layouts.
    """
    widgetClass = 'activeXTextClass'
    minor   = 1
    release = 1
    template   = 'text.edl'
   
    
    text      = pedlproperty(str, default='', doc='Text inside the label')
    fill      = pedlproperty(ColorChoice, doc='Background fill in the widget')
    linewidth = pedlproperty(int, default=0.,  doc='Stroke of surrounding border')
    alignment = pedlproperty(AlignmentChoice, default=AlignmentChoice.Center,
                             doc='Alignment of text within the widget')
    fontColor = pedlproperty(int, default=ColorChoice.Black,
                             doc='Color of the font inside the button')
   
    font = pedlproperty(Font.is_font, default=Font(size=12),
                        doc= 'Font as indicated by :class:`.Font`')

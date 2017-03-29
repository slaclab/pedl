"""
In order to represent EDM properties that are restricted to a specific set of
values, PEDL will have a corresponding ``Choice`` object. These are  Python ``Enum``
types, that wrap the underlying EDM property options with conveinent, tab
accessible attributes
"""
####################
# Standard Library #
####################
from enum import Enum

####################
#    Third Party   #
####################

####################
#     Package      #
####################

class ColorChoice(Enum):
    """
    Choices of Color available in EDM
    """
    White  = 0
    Grey   = 4
    Black  = 14
    Green  = 16
    Red    = 21
    Blue   = 26
    Cyan   = 31
    Yellow = 36
    Brown  = 43
    Purple = 47
    AMO    = 90
    MEC    = 83
    XCS    = 84
    SXR    = 85
    XPP    = 91
    CXI    = 92
    MFX    = 93


class AlignmentChoice(Enum):
    """
    Choices of Alignment in EDM
    """
    Left   = 'left'
    Center = 'center'
    Right  = 'right'
    Bottom = 'bottom'
    Top    = 'top'

class FontChoice(Enum):
    """
    Choices of Font in EDM
    """
    Helvetica             = 'helvetica'
    Utopia                = 'utopia'
    NewCenturySchoolbook  = 'new century schoolbook'
    Times                 = 'times'
    Courier               = 'courier'

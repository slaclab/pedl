from enum import Enum

class ColorChoice(Enum):

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
    Left   = 'left'
    Center = 'center'
    Right  = 'right'
    Bottom = 'bottom'
    Top    = 'top'

class FontChoice(Enum):
    Helvetica             = 'helvetica'
    Utopia                = 'utopia'
    NewCenturySchoolbook  = 'new century schoolbook'
    Times                 = 'times'
    Courier               = 'courier'

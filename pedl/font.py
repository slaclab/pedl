import math
from enum import Enum

from .widget  import Choice
from .choices import FontChoice

class Font:
    """
    Class to create an EDL font
    
    Parameters
    ----------
    size : int
        Size of the font, must be one of the appropriate size listed by
        :attr:`Font.sizes` otherwise it will be rounded.

    bold : bool
        Choice to have bold text

    italicized : bool
        Choice to have italic text
    
    color : :class:`.ColorChoice`
        Choice of text color. Black by default

    alignment : :class:`.AlignmentChoice
        Either an AlignmentChoice object or an appropriate value

    font : :class:`.FontChoice`
        Either a FontChoice object or an appropriate value
    """
    sizes = [8,10,12,14,18,24,32,48,72]

    #Defaults
    _size       = 18
    _italicized = False
    _bold       = False
    _font       = FontChoice.Helvetica

    def __init__(self, size=18, italicized=False,
                 bold=False,  font=FontChoice.Helvetica):

        self.size       = size
        self.bold       = bold
        self.font       = font
        self.italiczied = italicized

    @property
    def bold(self):
        """
        Choice to have bold text
        """
        return self._bold

    @bold.setter
    def bold(self, value):
        self._bold = bool(value)


    @property
    def italicized(self):
        """
        Choice to have italicized text
        """
        return self._italic

    @italicized.setter
    def italicized(self, value):
        self._italic = bool(value)


    def font(self):
        """
        Choice of font
        """
        return self._font

    @font.setter
    def font(self, value):
        return self._font = FontChoice(value)

    @property
    def size(self):
        """
        Size of the font
        """
        return self._size


    @size.setter
    def size(self, value):
        if value in self.sizes:
            self._size = float(value)
        else:
            print('Invalid size, rounding to nearest value')
            distance = [math.fabs(i-value) for i in self.sizes]
            self._size =  self.sizes[distance.index(min(distance))]   


    def tag(self):
        """
        Return the formatted Font specification

        Returns
        -------
        edm : str
        """

        #Bold tag
        if self.bold:
            bold = 'bold'
        else:
            bold = 'medium'

        #Italic tag
        if self.italicized:
            italic = 'i'

        else:
            italic = 'r'


        return '-'.join([self.font.value, bold, italic, self.size])






    def __repr__(self):
        return 'Font {} (Size : {}pt, Italic : {},'\
                'Bold {}, Color :{})'.format(self.font,
                                             self.size,
                                             self.italicized,
                                             self.bold,
                                            )

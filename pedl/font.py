import math
from enum import Enum

from .widget  import Choice
from .choices import ColorChoice, AlignmentChoice, FontChoice



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

    #Dimensions
    bold       = Dimension('bold', bool, False)
    italicized = Dimension('italicized', bool, False)
    color      = Choice('color', ColorChoice, ColorChoice.Black)
    alignment  = Choice('alignment', AlignmentChoice, AlignmentChoice.Left)
    font       = Font('font', FontChoice, FontChoice.Helvetica)

    def __init__(self, size=18, italicized=False,
                 bold=False, color=ColorChoice.Black,
                 alignment=AlignmentChoice.Left,
                 font=FontChoice.Helvetica):

        self.size       = size
        self.bold       = bold
        self.font       = font
        self.color      = color
        self.alignment  = alignment
        self.italicized = italicized
    


    def _tag(self):
        """
        Return the formatted Font specification

        Parameters
        ----------
        alignment : bool
            Include the command to align the text

        color : bool
            Include the command to color the text
        
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



    def __repr__(self):
        return 'Font {} (Size : {}pt, Italic : {},'\
                'Bold {}, Color :{})'.format(self.font,
                                             self.size,
                                             self.italicized,
                                             self.bold,
                                             self.color
                                            )

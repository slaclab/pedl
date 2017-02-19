from .widget  import Widget
from .choices import AlignmentChoice

class Layout(object):

    alignment = None

    def __init__(self, spacing=5):
        self.widgets = list()
        self.spacing = spacing


    def addWidget(self, widget):
        """
        Add a Widget to the Layout
        """
        if not isinstance(widget, Widget):
            raise TypeError('Must be an EDM Widget')

        self.widgets.append(widget)


    def addLayout(self, layout):
        """
        Add a child layout
        """
        if not isinstance(layout, Layout):
            raise TypeError('Must be an EDM Layout')
        self.widgets.append(layout)


    def setAlignment(self, align):
        """
        Set the Alignment

        Parameters
        ----------
        align : :class:`.AlignmentChoice`
            The choice of alignment
        """
        self.alignment = AlignmentChoice(align)



class HorizontalLayout(Layout):

    alignment = AlignmentChoice.Top


    def _place(self, y):
        if self.alignment == AlignmentChoice.Top:
            [widget.y = y for widget in self.widgets]
        
        elif self.alignment == AlignmentChoice.Bottom:
            [widget. = y for widget in self.widgets]

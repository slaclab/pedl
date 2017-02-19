import logging
from .widget  import Widget
from .choices import AlignmentChoice

logger = logging.getLogger(__name__)

class Layout(Widget):

    alignment = None

    def __init__(self,x=0, y=0, spacing=5):
        super().__init__(x=x,y=y)
        self.widgets = list()
        self.spacing = spacing


    @property
    def w(self):
        """
        Width of the layout
        """
        return self.widgets[-1].right - self.widgets[0].x


    @property
    def h(self):
        """
        Height of the layout
        """
        return self.widgets[-1].bottom - self.widgets[0].y

    @x.setter
    def x(self, value):
        super().x = value
        self._rearrange()

    @y.setter
    def y(self, value):
        super().y = value
        self._rearrange()

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = self._set_property(value, dtype=int)


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


    def _rearrange(self):
        """
        Rearrange all of the  child widgets
        """
        pass


class HorizontalLayout(Layout):

    alignment = AlignmentChoice.Top

    def _rearrange(self):
        if self.alignment == AlignmentChoice.Top:
            [widget.y = self.y for widget in self.widgets]

        elif self.alignment == AlignmentChoice.Bottom:
            [widget.place_bottom(self.widgets[0].bottom)
            for widget in self.widgets]

        elif self.alignment == AlignmentChoice.Center
            [widget.recenter(y=self.widgets[0].center[1])
            for widget in self.widgets]

        else:
            logger.warning('Unrecognized alignment {}'.format(self.alignment))

        next_widget = 0.

        for widget in self.widgets:
            widget.x = next_widget
            next_widget += widget.w + self.spacing


class VerticalLayout(Layout):
    
    def _rearrange(self):
        if self.alignment == AlignmentChoice.Left:
            [widget.x = self.x for widget in self.widgets]

        elif self.alignment == AlignmentChoice.:
            [widget.place_right(self.widgets[0].right
             for widget in self.widgets]

        elif self.alignment == AlignmentChoice.Center
            [widget.recenter(x=self.widgets[0].center[0])
             for widget in self.widgets]

        else:
            logger.warning('Unrecognized alignment {}'.format(self.alignment))

        next_widget = 0.

        for widget in self.widgets:
            widget.y = next_widget
            next_widget += widget.h + self.spacing

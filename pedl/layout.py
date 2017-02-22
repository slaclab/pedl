"""
PEDL uses a Qt inspired layout system. Not all of the feature set has been
implemented, but the basic concept is the same as well as much of the API.
There are three major layout types, :class:`.HBoxLayout`, :class:`.VBoxLayout`
and finally :class:`.StackLayout`. The two former layout types are borrowed
directly from Qt, you simply add widgets and they are aligned and placed in
such a way that they are either in a vertical or horizontal line. Finally,
because EDM widgets tend to need to be stacked on top of each other, the
:class:`.StackLayout` can be used to handle these kind of situations.

Far more complex layouts are possible by using :meth:`Layout.addLayout` to
nest layouts inside of each other. This allows the user to maintain a master
layout composed of widgets and smaller layouts that can then be applied to a
widget by using the :meth:`.Designer.setLayout`
"""
import logging
from .widget  import PedlObject
from .choices import AlignmentChoice

logger = logging.getLogger(__name__)

class Layout(PedlObject):
    """
    Parameters
    ----------
    x : int, optional
        Starting X position of the layout

    y : int, optional
        Starting Y position of the layout
    """
    #Presets
    alignment = None
    _spacing  = 5

    def __init__(self,x=0, y=0):
        super().__init__(x=x,y=y)
        self.widgets = list()
        self.layouts = list()

    @property
    def w(self):
        """
        Width of the layout
        """
        return (max([w.right for w in self.widgets]) 
              - min([w.x     for w in self.widgets]))


    @property
    def h(self):
        """
        Height of the layout
        """
        return (max([w.bottom for w in self.widgets])
              - min([w.y      for w in self.widgets]))

    @property
    def x(self):
        """
        Horizontal position
        """
        return super().x


    @x.setter
    def x(self, value):
        #Make sure to rearrange widgets
        super().x.fset(value)
        self._rearrange()
    
    @property
    def y(self):
        """
        Vertical position
        """
        return super().y

    @y.setter
    def y(self, value):
        #Make sure to rearrange widgets
        super().y.fset(value)
        self._rearrange()


    @property
    def spacing(self):
        """
        Spacing between widgets
        """
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = self._set_property(value, dtype=int)


    def addWidget(self, widget):
        """
        Add a Widget to the Layout

        Parameters
        ----------
        widget : :class:`.Widget`
            EDM Widget
        """
        if not isinstance(widget, Widget):
            raise TypeError('Must be an EDM Widget')

        self.widgets.append(widget)


    def addLayout(self, layout):
        """
        Add a child layout

        Parameters
        ----------
        layout : :class:`.Layout`
            Nested layout to add
        """
        if not isinstance(layout, Layout):
            raise TypeError('Must be an EDM Layout')

        self.layouts.append(layout)


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


class HBoxLayout(Layout):
    """
    Layout for horizontally placed widgets
    """
    alignment = AlignmentChoice.Top

    def _rearrange(self):
        next_widget = self.x

        for widget in self.widgets:
            #Align Widget
            if self.alignment == AlignmentChoice.Top:
                widget.y = self.y

            elif self.alignment == AlignmentChoice.Bottom:
                widget.place_bottom(self.widgets[0].bottom)

            elif self.alignment == AlignmentChoice.Center:
                widget.recenter(y=self.widgets[0].center[1])

            else:
                logger.warning('Unrecognized alignment {}'.format(self.alignment))
            #Place Widget
            widget.x = next_widget
            next_widget += widget.w + self.spacing


class VBoxLayout(Layout):
    """
    Layout for vertically placed widgets
    """
    def _rearrange(self):
        next_widget = self.y
        
        for widget in self.widgets:
            if self.alignment == AlignmentChoice.Left:
                widget.x = self.x

            elif self.alignment == AlignmentChoice.Right:
                widget.place_right(self.widgets[0].right)

            elif self.alignment == AlignmentChoice.Center:
                widget.recenter(x=self.widgets[0].center[0])

            else:
                logger.warning('Unrecognized alignment {}'.format(self.alignment))

            widget.y = next_widget
            next_widget += widget.h + self.spacing


class StackLayout(Layout):
    """
    Layout for stacked widgets
    """
    _spacing   = None
    _alignment = AlignmentChoice.Center
    def _rearrange(self):
        ld = self.widgets[0]

        for widget in self.widgets:

            if self.alignment == AlignmentChoice.Left:
                w.x = ld.x
                w.recenter(y=ld.center[1])

            elif self.alignment == AlignmentChoice.Right:
                w.place_right(x=ld.right)
                w.recenter(y=ld.center[1])

            elif self.alignment == AlignmentChoice.Top:
                w.recenter(x=ld.center[0])
                w.y = ld.y

            elif self.alignment == AlignmentChoice.Bottom:
                w.recenter(x=ld.center[0])
                w.place_bottom(y=ld.bottom)

            elif self.alignment == AlignmentChoice.Center:
                w.recenter(ld.center)

            else:
                logger.warning('Unrecognized alignment {}'.format(self.alignment))
                w.recenter(ld.center)

    #This annoying I have to do this to super setter method 
    @property
    def spacing(self):
        return super().spacing


    @spacing.setter
    def spacing(self, value):
        raise NotImplementedError


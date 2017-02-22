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
from .widget  import Widget, PedlObject
from .choices import AlignmentChoice

logger = logging.getLogger(__name__)

class Layout(PedlObject):
    obj = 'Layout'
    """
    Parameters
    ----------
    x : int, optional
        Starting X position of the layout

    y : int, optional
        Starting Y position of the layout
    """
    _spacing   = 5
    _alignment = None
    def __init__(self,x=0, y=0):
        self.widgets = list()
        super().__init__(x=x,y=y)


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
        if value != self.x:
            #Set position internally
            super(Layout, self.__class__).x.fset(self, value)
            if self.widgets:
                #Move first widget
                self.widgets[0].x = value
                #Rearrange following widgets
                self._rearrange()

    @property
    def y(self):
        """
        Vertical position
        """
        return super().y

    @y.setter
    def y(self, value):
        if value != self.y:
            #Set position internally
            super(Layout, self.__class__).y.fset(self, value)
            if self.widgets:
                #Move first widget
                self.widgets[0].y = value
                #Rearrange following widgets
                self._rearrange()


    @property
    def spacing(self):
        """
        Spacing between widgets
        """
        return self._spacing


    @spacing.setter
    def spacing(self, value):
        if value != self.spacing:
            self._spacing = self._set_property(value, dtype=int)
            self._rearrange()


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

        #Note as child widget
        widget.parent = self

        #Add to widget
        self.widgets.append(widget)

        #Redraw
        self._rearrange()


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

        #Note as child layout
        layout.parent = self

        #Add to Widget
        self.widgets.append(layout)

        #Redraw
        self._rearrange()


    @property
    def alignment(self):
        """
        Alignment of the Layout selected from :class:`.AlignmentChoice`
        """
        return self._alignment


    @alignment.setter
    def alignment(self, align):
        if align != self.alignment:
            self._alignment = AlignmentChoice(align)
            self._rearrange()


    def _rearrange(self):
        """
        Rearrange all of the  child widgets
        """
        logger.debug("Rearranging layout")


class HBoxLayout(Layout):
    """
    Layout for horizontally placed widgets
    """
    _alignment = AlignmentChoice.Top
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
                logger.warning('Unsupported alignment {}'.format(self.alignment))
            #Place Widget
            widget.x = next_widget
            next_widget += widget.w + self.spacing


class VBoxLayout(Layout):
    """
    Layout for vertically placed widgets
    """
    _alignment = AlignmentChoice.Left
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
                logger.warning('Unsupported alignment {}'.format(self.alignment))

            widget.y = next_widget
            next_widget += widget.h + self.spacing


class StackLayout(Layout):
    """
    Layout for widgets placed on top of each other
    """
    _spacing   = None
    _alignment = [AlignmentChoice.Center]

    #This is annoying I have to do this to super setter method 
    @property
    def alignment(self):
        """
        List of alignments

        The alignment specification works slightly differently in the case of the
        stack layout, because there are two possible axes to specify. This
        means that you may enter an list of Alignment options to be more
        specific in your widget placement. By default, no option is given for
        an axis, the layout assumes you want the widgets centered

        Example
        -------
        .. code::

            #Centered on both axes
            layout.alignment = AlignmentChoice.Center

            #Top-Right Corner
            layout.alignment = [AlignmentChoice.Top, AlignmentChoice.Right]

            #Left-Side Aligned, Centered in Vertical
            layout.alignment = [AlignmentChoice.Left]
        """
        return self._alignment


    @alignment.setter
    def alignment(self, align):
        if align != self._alignment:

            try:
                self._alignment = [AlignmentChoice(a) for a in align]

            except TypeError:
                self._alignment = [AlignmentChoice(align)]

            self._rearrange()


    def _rearrange(self):
        ld = self.widgets[0]

        for w in self.widgets:

            #Place X axis
            if AlignmentChoice.Left in self.alignment:
                w.x = ld.x

            elif AlignmentChoice.Right in self.alignment:
                w.place_right(x=ld.right)

            else:
                w.recenter(x=ld.center[0])

            #Place Y axis
            if AlignmentChoice.Top in self.alignment:
                w.y = ld.y

            elif AlignmentChoice.Bottom in self.alignment:
                w.place_bottom(y=ld.bottom)

            else:
                w.recenter(y=ld.center[1])

        if self.parent:
            parent._rearrange()

    #This is annoying I have to do this to super setter method 
    @property
    def spacing(self):
        return super().spacing


    @spacing.setter
    def spacing(self, value):
        raise NotImplementedError


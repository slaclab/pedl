class Visibility:
    """
    Visibility Settings for Widget

    This supplies a simple interface for handling the visibility settings
    for a widget. EDM depends on a Visibility PV and a given range to determine
    whether a Widget will be shown or not. In the most basic setup, if the PV
    value is within the given range, the widget is shown. However, you can also
    invert this by setting :attr:`.inverted` to True, and use the given range
    to hide the Widget

    Before drawing, the :class:`.pedl.Designer` will check the :attr:`.valid`
    flag to make sure that information has been properly entered, and the range
    makes logical sense.

    Parameters
    ----------
    pv : str
        PV to monitor for Visibility Settings

    min:  int, float, optional
        Mininum value to display Widget (inclusive)

    max : int, float, optional
        Maximum value to display Widget (exclusive)

    Attributes
    ----------
    pv : str
        PV to monitor for Visibility Settings

    min:  int, float
        Mininum value to display Widget (inclusive)

    max : int, float
        Maximum value to display Widget (exclusive)
    """
    def __init__(self, pv=None, min=None, max=None, inverted=False):
        self.pv  = pv
        self.min = min
        self.max = max
        self._inverted = inverted


    @property
    def inverted(self):
        """
        Whether the widget should be visible when the PV value enters the given
        range
        """
        return self._inverted

    @inverted.setter
    def inverted(self, value):
        self._inverted = bool(value)


    @property
    def entered(self):
        """
        Whether any Visibility information has been entered
        """
        return any([self.pv, self.min, self.max])


    @property
    def valid(self):
        """
        Valid Visibility Information
        """
        if not self.pv:
            return False

        if self.min is not None and self.max is not None:
            return self.min < self.max

        elif self.min is not None or self.max is not None:
            return True

        else:
            return False

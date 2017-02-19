import logging

logger = logging.getLogger(__name__)

class Visibility:
    """
    Visibility Settings for Widget
    """
    def __init__(self, pv=None, min=None, max=None):
        self.pv  = pv
        self.min = min
        self.max = max


    @property
    def valid(self):
        """
        Valid Visibility Information
        """
        if not self.pv:
            return False

        if self.min and self.max:
            return self.min < self.max

        elif self.min or self.max:
            return True

        else:
            return False

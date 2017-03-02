from .               import choices
from .font           import Font
from .widget         import Widget
from .widgets.shape  import Rectangle, Circle
from .utils          import Visibility, launch
from .designer       import Designer
from .layout         import VBoxLayout, HBoxLayout, StackLayout

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

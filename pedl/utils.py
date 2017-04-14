"""
PEDL Utilities
"""
############
# Standard #
############
import os
import re
import sys
import math
import copy
import logging
import subprocess
from enum import Enum
from distutils.spawn import find_executable
###############
# Third Party #
###############


##########
# Module #
##########
from .choices import FontChoice
logger = logging.getLogger(__name__)


def launch(path, wait=True, wd=None, **kwargs):
    """
    Launch an EDL file

    Parameters
    ----------
    path : str
        Path to file

    wd : str, optional
        Working directory to launch screen, otherwise the current directory
        is used

    wait : bool, optional
        Block the main thread while the EDM preview is open

    kwargs : optional
        Represent EDM macros as keyword arguments

    Returns
    -------
    proc : ``subprocess.Popen``
        Process containing EDM launch

    Raises
    ------
    FileNotFoundError:
        If the .edl file does not exist

    OSError:
        If the ``edm`` executable is not in the system path

     Example
    -------
    .. code::

        edm_proc = launch('path/to/my.edl', MACRO='TST:MACRO')
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    edm_args = ['edm', '-x', '-eolc']

    if kwargs:
        edm_args.append(','.join(['='.join([key,value])
                        for (key,value) in kwargs.items()]))

    edm_args.append(path)

    try:
        logger.debug("Launching {} with the following command {}"
                     "".format(path, edm_args))
        proc = subprocess.Popen(edm_args, cwd=wd, stdout=None)

        if wait:
            proc.wait()

    except OSError:
        if not find_executable('edm'):
            raise OSError('EDM is not in current environment')

        raise

    except KeyboardInterrupt:
        print('Preview aborted ...')
        proc.terminate()

    return proc


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
    makes logical sense. By default, the max is set to :attr:`.default_max`,
    as the EDM interpreter effectively will not show a PV who has only a
    minimum Visibility range set.

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

    default_max : int
        Default maximum value if not max is specified
    """
    default_max = 1000

    def __init__(self, pv=None, min=None, max=None, inverted=False):
        self.pv  = pv
        self.min = min
        self.max = max or self.default_max
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
        return any([self.pv, self.min, self.max!=self.default_max])


    @property
    def valid(self):
        """
        Valid Visibility Information
        """
        if not self.pv:
            return False

        if self.min is not None:
            return self.min < self.max

        return True


    @classmethod
    def is_visibility(cls, vis):
        """
        Create a representation of Visibility settings from a given set of
        information

        If the provided argument is already Visibility object, it is simply
        returned, otherwise dicts and iterables are attempted to be converted
        into a Visibility. If ``None`` is provided, Visbility is returned with only
        default settings

        Parameters
        ----------
        vis : :class:`.Visibility`, NoneType, dict, or iterable
            Visibilility specification to convert


        Returns
        -------
        font : :class:`.Font`
            Converted Font

        Raises
        ------
        ValueError:
            If the given specification can not be converted
        """
        if isinstance(vis, cls):
            return copy.copy(vis)

        elif vis == None:
            return Visibility()

        try:
            if isinstance(vis, dict):
                vis = cls(**vis)

            else:
                vis = cls(*vis)

        except TypeError:
            raise ValueError("Invalid visibility '{}'".format(vis))

        return vis


    def __copy__(self):
        return Visibility(pv=self.pv, min=self.min,
                          max=self.max, inverted=self.inverted)

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

    font : :class:`.FontChoice`
        Either a FontChoice object or an appropriate value

    Attributes
    ----------
    sizes : list
        Available font sizes within EDM
    """
    sizes = [8,10,12,14,18,24,32,48,72]

    #Defaults
    _size   = 18
    _italic = False
    _bold   = False
    _font   = FontChoice.Helvetica

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

    @property
    def font(self):
        """
        Choice of font from :class:`.FontChoice`
        """
        return self._font

    @font.setter
    def font(self, value):
        self._font = FontChoice(value)

    @property
    def size(self):
        """
        Size of the font, restricted to :attr:`.sizes`
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

    @property
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

        #Trailing zero on size
        size = '{:.1f}'.format(self.size)

        return '-'.join([self.font.value, bold, italic, size])

    @classmethod
    def is_font(cls, font):
        """
        Create a font from a given set of information

        If the provided argument is already a Font, it is simply returned,
        otherwise dicts and iterables are attempted to be converted into a
        Font. If ``None`` is provided, a Font is returned with only default
        settings

        Parameters
        ----------
        font : :class:`.Font`, NoneType, dict, or iterable
            Font specification to convert


        Returns
        -------
        font : :class:`.Font`
            Converted Font

        Raises
        ------
        ValueError:
            If the given specification can not be converted
        """
        if isinstance(font, cls):
            return copy.copy(font)

        elif font == None:
            return Font()

        try:
            if isinstance(font, dict):
                font = cls(**font)

            else:
                font = cls(*font)

        except TypeError:
            raise ValueError("Invalid font '{}'".format(font))

        return font

    def __repr__(self):
        return 'Font {} (Size : {}pt, Italic : {},'\
                'Bold {})'.format(self.font,
                                  self.size,
                                  self.italicized,
                                  self.bold)

    def __copy__(self):
        return Font(size=self.size, italicized=self.italicized,
                    bold=self.bold, font=self.font)


class pedlproperty:
    """
    Reimplementation of Python property

    This allows the flagging of certain properties as pertinent to PEDL
    specifically, as well as the enforcement of types.

    Parameters
    ----------
    _type : type
        Desired type. The only caveat is bool variables should still be set as
        ``int`` because EDM accepts binary instead of True / False keywords

    default : value, optional
        Default value to intialize the property with

    fset : callable, optional
        Function to overwrite default set method

    fget : callable, optional
        Function to overwrite default get method

    cd : callable, optional
        Function to be run after the fset changes the property value
    
    doc : str, optional
        Short doc-string to describe the property
    """
    def __init__(self, _type, default=None,
                 fset=None, fget=None,
                 cb=None, doc=None):
        #Property information
        self.type    = _type
        self.cb      = cb
        self.default = default
        #Getter and Setter methods
        self.fget = fget
        self.fset = fset
        #Store docstring internally
        self.__doc__ =  doc


    def __get__(self, instance, owner):
        #Allow override of get method
        if self.fget:
            self.fget(instance, owner)

        else:
            #If requesting class attribute, return pedlproperty
            if instance is None:
                return self

            #Otherwise, lookup in instance dictionary
            return instance.attributes[self.attr]


    def __set__(self, instance, value):
        #Allow override of set method
        if self.fset:
            self.fset(instance, value)

        #Enforce value
        else:
            if value is not None and self.type is not None:
                value = self.type(value)

            #Store previous value for comparison
            previous = instance.attributes.get(self.attr)
            instance.attributes[self.attr] = value 

            #Run callback on value changed
            if previous != value and self.cb:
                self.cb(instance)


    def getter(self, fget):
        return type(self)(self.type, default=self.default,
                          fget=fget, fset=self.fset,
                          cb=self.cb, doc=self.__doc__)

    def setter(self, fset):
        return type(self)(self.type, default=self.default,
                          fget=self.fget, fset=fset,
                          cb=self.cb, doc=self.__doc__)

    def callback(self, cb):
        return type(self)(self.type, default=self.default,
                          fget=self.fget, fset=self.fset,
                          cb=cb, doc=self.__doc__)


def find_screen_size(handle):
    """
    Find the screen size of a previously written EDL file

    Parameters
    ----------
    handle : file-like object
        EDL path to read screen size

    Returns
    -------
    dimensions : tuple
        Width and height of screen

    Raises
    ------
    ValueError:
        Raised if no screen information is found
    """
    #Compile overall screen regex match
    tpl = re.compile(r'beginScreenProperties(?:.+)'
                      'w (\d+)\nh (\d+)'
                      '(?:.+)endScreenProperties',
                      flags=re.DOTALL)
    #Search for screen properties in file
    with handle as f:

        props = tpl.search(f.read())

    if not props:
        raise ValueError("No screen dimension information "
                         "found within file")

    return tuple(int(d) for d in props.groups())


class LocalPv(object):
    """
    Representation of local EDM Pv

    These PVs are internal to EDM, include the ```LOC\prefix`` and can be of
    type ``float``, ``int`` or ``string``. EDM creates a local PV the first
    time it is encountered. If types or values differ between the two
    declarations, the first one wins.
    
    Parameters
    ----------
    name : str
        Name of PV to be instantiated

    value : int, float, list, or str, optional
        Default value of LocalPV 
    
    Raises
    ------
    TypeError:
        If the value is of an supporte type
    """
    pv_types = {str : 's', int : 'i', float : 'd'}

    def __init__(self, name, value=None):

        if type(value) not in self.pv_types:
            raise TypeError("Not a valid local PV "
                            "type for {}".format(value))

        #PV Information
        self.name  = name
        self.value = value


    @property
    def declaration(self):
        """
        Tag for the local PV
        """
        name = 'LOC\\\\{}'.format(self.name)

        if self.value is not None:
            name += '={}:{}'.format(self.pv_types[type(self.value)],
                                    self.value)

        return name


    def __str__(self):
        return self.declaration


class LocalEnumPv(LocalPv):
    """
    Representation of Local EnumPV

    Compared to other Enum types, local Enum Pvs are slightly more complex as
    you can specify a number of states and then select one to be the default
    value upon instantiation. Instead of using an Enum to represent this in
    Python, a list of states is given, and one is specified as the default
    value

    Parameters
    ----------
    name : str
        Name of PV to be instantiated

    states : list
        Possible states for enum PV

    value : str, optional
        Name of state to instantiate Enum with. By default, the first state is
        taken
    """
    pv_types = {int : 'e', list : 'e'}

    def __init__(self, name, states, value=None):
        self.states = states

        #Grab index of default
        if not value:
            value = 0
        else:
            value = states.index(value)

        super(LocalEnumPv, self).__init__(name, value)


    @property
    def declaration(self):
        """
        Tag to declare the local PV
        """
        return super().declaration + ',' + ','.join(self.states)

############
# Standard #
############
import os.path

###############
# Third Party #
###############
import pytest
from six import StringIO

##########
# Module #
##########
from pedl.utils import find_screen_size


def test_find_screen_size():
    #Absolute file path
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'test.edl')
    #Find screen size
    f = open(path,'r')
    assert find_screen_size(f) == (780, 1125)

    #Try and find invalid screen size
    f = StringIO('Invalid')

    with pytest.raises(ValueError):
        find_screen_size(f)

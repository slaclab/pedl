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
from pedl.utils import LocalPv, LocalEnumPv, find_screen_size


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

def test_local_pv():
    pv = LocalPv('stringPv', 'this is a string')
    assert str(pv) == 'LOC\\stringPv=s:this is a string'

    with pytest.raises(TypeError):
        pv = LocalPv('fail', dict())

def test_local_enum():
    pv = LocalEnumPv('enumPv', ['zero','one','two'], value='two')
    assert str(pv) == 'LOC\\enumPv=e:2,zero,one,two'

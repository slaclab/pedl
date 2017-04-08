############
# Standard #
############
import os.path
import logging

###############
# Third Party #
###############
import pytest

##########
# Module #
##########
import pedl
from pedl.widgets import EmbeddedWindow
from pedl.widgets.embedded import Display

logger = logging.getLogger(__name__)

def test_from_edl():
    d = Display.from_edl('testing/name.edl')
    assert d.name   == 'name'
    assert d.path   == 'testing/name.edl'
    assert d.macros == None


def test_resize():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'test.edl')
    emb = EmbeddedWindow(displays = [path],
                         autoscale=False)
    emb.resize()
    assert emb.w == 780
    assert emb.h == 1125

def test_addDisplay():
    emb = EmbeddedWindow(autoscale=False)
    emb.addDisplay('testing/name.edl')
    assert emb.count == 1
    assert emb.displays[0].path == 'testing/name.edl'

def test_embedded_rendering():
    emb = EmbeddedWindow(displays=['tests/test.edl'],
                         autoscale=False, w=1000, h=1200)
    d = pedl.Designer()
    assert d.render(emb) == edl

edl ='''\
# (activePipClass)
object activePipClass
beginObjectProperties
major 4
minor 1
release 0
x 0
y 0
w 1000
h 1200
fgColor index 14
bgColor index 0
topShadowColor index 0
botShadowColor index 14
displaySource "menu"
filePv "LOC\\emb-window=i:0"
sizeOfs 99
numDsps 1
displayFileName {
  0 "tests/test.edl"
}
menuLabel {
  0 "test"
}
symbols {
  0 "None"
}
endObjectProperties'''

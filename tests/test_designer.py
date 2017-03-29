import os
import time
import pytest
from distutils.spawn import find_executable 

import pedl
import conftest
import tempfile
from pedl.choices import FontChoice


requires_edm = pytest.mark.skipif(find_executable('edm') == None,
                                  reason='EDM not found in current'\
                                         ' environment')

def test_designer_init():
    with pytest.raises(FileNotFoundError):
        d = pedl.Designer(template_dir='NOT/A/DIR')

    d = pedl.Designer()
    assert os.path.exists(d.env.loader.searchpath[0])


def test_addWidget():
    d = pedl.Designer()
    w = pedl.Widget()
    d.addWidget(w)
    assert d.widgets == [w]

    with pytest.raises(TypeError):
        d.addWidget(4)

def test_set_layout():
    d = pedl.Designer()
    l = pedl.StackedLayout()
    l.addWidget(pedl.Widget(w=100, h=100))
    d.window.setLayout(l, resize=True)
    assert d.widgets == [l]
    assert d.window.w == 110 
    assert d.window.h == 110 

def test_recursive_widget_search():
    d  = pedl.Designer()
    l  = pedl.StackedLayout()
    w1 = pedl.Widget()
    w2 = pedl.Rectangle(name='RECT')
    w3 = pedl.Widget()
    l.addWidget(w1)
    l.addWidget(w2)
    d.window.setLayout(l)
    d.addWidget(w3)
    assert d.widgets == [l,w3]
    assert d.findChildren() == [w1,w2,w3]
    assert d.findChildren(name='RECT') == [w2]
    assert d.findChildren(_type=pedl.Rectangle) == [w2]



def test_screen_render():
    d = pedl.Designer()
    #Change Screen Attributes
    d.window.w, d.window.h = 780, 1125
    d.window.name = 'Test'
    #Render
    assert d.render(d.window) == conftest.window_edl

def test_widget_render():
    d = pedl.Designer()
    w = pedl.Widget(name='Rectangle')
    assert d.render(w) == conftest.widget_edl

@requires_edm
def test_launch():
    d    = pedl.Designer()
    with pytest.raises(FileNotFoundError):
        pedl.launch('NOT.edl')

    edl  = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test.edl')
    proc = pedl.launch(edl, MACRO='TST:MACRO',wait=False)
    assert not proc.poll()
    proc.terminate()
    #Wait for process to die
    time.sleep(0.5)
    #Check for exit code
    assert proc.poll() == -15

@requires_edm
def test_exec():
    d    = pedl.Designer()
    proc = d.exec_(wait=False)
    assert not proc.poll()
    proc.terminate()




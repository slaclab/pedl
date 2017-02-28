import os
import pytest
from distutils.spawn import find_executable 

import pedl
from pedl.choices import FontChoice

edm_dependent = pytest.mark.skipif(find_executable('edm') != None,
                                   reason='EDM not found in current'\
                                           ' environment')

def test_designer_init():
    with pytest.raises(FileNotFoundError):
        d = pedl.Designer(template_dir='NOT/A/DIR')

    d = pedl.Designer()
    assert os.path.exists(d.env.loader.searchpath[0])


def test_attributes():
    d = pedl.Designer()
    assert d.w == 750
    d.w = 800
    assert d.w == 800
    assert d.h == 1100
    d.w = 1200
    assert d.w == 1200
    assert d.font == pedl.choices.FontChoice.Helvetica
    d.font = FontChoice.Utopia
    assert d.font == FontChoice.Utopia
    d.font = pedl.Font(font=FontChoice.Helvetica)
    assert d.font == FontChoice.Helvetica

def test_add_widget():
    d = pedl.Designer()
    w = pedl.Widget()
    d.addWidget(w)
    assert d.widgets == [w]

    with pytest.raises(TypeError):
        d.addWidget(4)

def test_set_layout():
    d = pedl.Designer()
    l = pedl.StackLayout()
    d.setLayout(l)
    assert d.widgets == [l]

    with pytest.raises(TypeError):
        d.setLayout(4)

def test_recursive_widget_search():
    d  = pedl.Designer()
    l  = pedl.StackLayout()
    w1 = pedl.Widget()
    w2 = pedl.Widget()
    w3 = pedl.Widget()
    l.addWidget(w1)
    l.addWidget(w2)
    d.setLayout(l)
    d.addWidget(w3)
    assert d.widgets == [l,w3]
    assert d.all_widgets == [w1,w2,w3]




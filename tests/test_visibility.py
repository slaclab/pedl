import pytest
import pedl

def test_invert():
    vis = pedl.Visibility()
    assert vis.inverted == False
    vis.inverted = True
    assert vis.inverted

def test_entered():
    vis = pedl.Visibility()
    assert not vis.entered
    vis.min = 1
    assert vis.entered
    vis.max = 2
    assert vis.entered

def test_valid():
    vis = pedl.Visibility()
    #Test no information
    assert not vis.valid

    #Test no range information
    vis.pv = 'TST:PV'
    assert not vis.valid

    #Test valid
    vis.min, vis.max = 0,4
    assert vis.valid

    #Test conflicting range
    vis.max = -1
    assert not vis.valid

    #Test open ended range
    vis.max = None
    assert vis.valid

def test_template():
    d = pedl.Designer()
    w = pedl.Widget()
    assert 'vis' not in d.render(w)
    w.visibility.pv = 'TST:PV'
    w.visibility.min, w.visibility.max = 1,2
    assert 'visPv TST:PV' in d.render(w)
    assert 'visMax 2' in d.render(w)
    assert 'visMin 1' in d.render(w)
    w.visibility.inverted = True
    assert 'visInverted' in d.render(w)


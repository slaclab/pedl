import pytest
import pedl

@pytest.fixture(scope='function')
def pedl_obj():
    return pedl.widget.PedlObject('xxx', x=50, y=50,
                                  w=100, h=100)


def test_x(pedl_obj):
    assert pedl_obj.x == 50
    pedl_obj.x = 100
    assert pedl_obj.x == 100
    
def test_y(pedl_obj):
    assert pedl_obj.y == 50
    pedl_obj.y = 100
    assert pedl_obj.y == 100

def test_w(pedl_obj):
    assert pedl_obj.w == 100
    pedl_obj.w = 150
    assert pedl_obj.w == 150

def test_h(pedl_obj):
    assert pedl_obj.h == 100
    pedl_obj.h = 150
    assert pedl_obj.h == 150

def test_framing(pedl_obj):
    assert pedl_obj.bottom == 150
    assert pedl_obj.right  == 150
    assert pedl_obj.center == (100, 100)
    pedl_obj.w = 75
    assert pedl_obj.center == (88, 100)

def test_placements(pedl_obj):
    pedl_obj.place_bottom(200)
    assert pedl_obj.y == 100
    pedl_obj.place_right(150)
    assert pedl_obj.x == 50
    pedl_obj.recenter(x=50, y=50)
    assert pedl_obj.x == 0
    assert pedl_obj.y == 0




import pytest
import pedl

def test_fill():
    widget = pedl.widgets.shape.Shape()
    assert widget.fill == None
    widget.fill = 93
    assert widget.fill == pedl.choices.ColorChoice.MFX
    widget.fill = pedl.choices.ColorChoice.Blue
    assert widget.fill == pedl.choices.ColorChoice.Blue
    widget.fill = None
    assert widget.fill == None

def test_line_color():
    widget = pedl.widgets.shape.Shape()
    widget.lineColor = 93
    assert widget.lineColor == pedl.choices.ColorChoice.MFX
    widget.lineColor = pedl.choices.ColorChoice.Blue
    assert widget.lineColor == pedl.choices.ColorChoice.Blue

def test_line_width():
    widget = pedl.widgets.shape.Shape()
    widget.lineWidth = 4
    assert widget.lineWidth == 4


def test_lines_widget():
    v = pedl.widgets.shape.Lines(points=[(0,0),(5,0),(5,10),(0,10),(0,0)])
    assert v.x == 0
    assert v.y == 0
    assert v.w == 5
    assert v.h == 10

    v.w = 10
    v.h = 25
    assert v.x == 0
    assert v.y == 0
    assert v.w == 10
    assert v.h == 25

    v.x = 15
    v.y = 25
    assert v.x == 15
    assert v.y == 25
    assert v.w == 10
    assert v.h == 25


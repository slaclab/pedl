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

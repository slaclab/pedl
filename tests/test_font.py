import pedl
import pytest

@pytest.fixture
def font():
    return pedl.Font()

def test_bold(font):
    assert font.bold == False
    font.bold = True
    assert font.bold

def test_italic(font):
    assert font.italicized == False
    font.italicized = True
    assert font.italicized

def test_font(font):
    assert font.font == pedl.choices.FontChoice.Helvetica
    font.font = pedl.choices.FontChoice.Utopia
    assert font.font == pedl.choices.FontChoice.Utopia
    font.font = 'helvetica'
    assert font.font == pedl.choices.FontChoice.Helvetica

def test_size(font):
    assert font.size == 18
    font.size = 12
    assert font.size == 12
    font.size = 19
    assert font.size == 18

def test_tag(font):
    assert font.tag == 'helvetica-medium-r-18.0'
    font.size = 8
    font.font = 'utopia'
    font.bold, font.italicized = True, True
    assert font.tag == 'utopia-bold-i-8.0'

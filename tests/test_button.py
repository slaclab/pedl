############
# Standard #
############

###############
# Third Party #
###############

##########
# Module #
##########
import pedl


def test_message():
    w = pedl.widgets.MessageButton(value=0, controlPv='LOC\\\\intPv=i:0',
                                   label='here', w=100, h=100)
    d = pedl.Designer()
    assert d.render(w) == message_edl

def test_menu():
    w = pedl.widgets.MenuButton(name="Menu Button",
                                x=24,y=148,w=200,h=105,
                                controlPv='PV:FAKE')
    w.lineColor = pedl.choices.ColorChoice.Black
    d = pedl.Designer()
    assert d.render(w) == menu_edl


def test_message_buttonize():
    w = pedl.Widget(w=50,h=75)
    l = pedl.widgets.MessageButton.buttonize(w, controlPv='PV:FAKE',value=10)
    assert isinstance(l, pedl.StackedLayout)
    assert l.widgets[0].controlPv == 'PV:FAKE'
    assert l.widgets[0].value == 10
    assert l.widgets[0].w == 50
    assert l.widgets[0].h == 75
    assert l.widgets[1].w == 50
    assert l.widgets[1].h == 75

def test_menu_buttonize():
    w = pedl.Widget(w=50,h=75)
    l = pedl.widgets.MenuButton.buttonize(w, controlPv='PV:FAKE')
    assert isinstance(l, pedl.StackedLayout)
    assert l.widgets[0].controlPv == 'PV:FAKE'
    assert l.widgets[0].w == 50
    assert l.widgets[0].h == 75
    assert l.widgets[1].w == 50
    assert l.widgets[1].h == 75



message_edl= """\
# (activeMessageButtonClass)
object activeMessageButtonClass
beginObjectProperties
major 4
minor 1
release 0
x 0
y 0
w 100
h 100
fgColor index 14
onColor index 4
offColor index 4
topShadowColor index 4
botShadowColor index 4
font helvetica-medium-r-18.0
controlPv LOC\\\\intPv=i:0
pressValue 0
onLabel here
offLabel here
endObjectProperties"""


menu_edl ="""\
# (Menu Button)
object activeMenuButtonClass
beginObjectProperties
major 4
minor 0
release 0
x 24
y 148
w 200
h 105
fgColor index 14
bgColor index 4
topShadowColor index 14
botShadowColor index 14
inconsistentColor index 4
font helvetica-medium-r-18.0
controlPv PV:FAKE
endObjectProperties"""

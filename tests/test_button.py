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

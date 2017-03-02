import logging

#Configure Logging
logging.getLogger('pedl').setLevel(logging.DEBUG)
logging.basicConfig()

window_edl = """\
4 0 1
beginScreenProperties
major 4
minor 0
release 1
x 0
y 0
w 780
h 1125
font "helvetica-medium-r-18.0"
ctlFont "helvetica-medium-r-18.0"
btnFont "helvetica-medium-r-18.0"
fgColor index 14
bgColor index 4
textColor index 14
ctlFgColor1 index 14
ctlFgColor2 index 0
ctlBgColor1 index 0
ctlBgColor2 index 14
topShadowColor index 0
botShadowColor index 14
title "Test"
showGrid
snapToGrid
gridSize 4
endScreenProperties"""

widget_edl = """\
# (Rectangle)
object None
beginObjectProperties
major 4
minor 1
release 1
x 0
y 0
w 0
h 0
endObjectProperties"""

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

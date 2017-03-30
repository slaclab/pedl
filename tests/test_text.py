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
from pedl.choices import AlignmentChoice

def test_text():
    w = pedl.widgets.StaticText(w=56, h=21, text='LABEL', lineWidth=3,
                                alignment=AlignmentChoice.Right)

    d = pedl.Designer()
    assert d.render(w) == text_edl

text_edl="""\
# (activeXTextClass)
object activeXTextClass
beginObjectProperties
major 4
minor 1
release 1
x 0
y 0
w 56
h 21
font "helvetica-medium-r-12.0"
fontAlign "right"
fgColor index 14
bgColor index 0
useDisplayBg
value {
  "LABEL"
}
border
lineWidth 3
endObjectProperties"""

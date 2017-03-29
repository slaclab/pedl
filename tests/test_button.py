"""
Module Docstring
"""
############
# Standard #
############
import logging

###############
# Third Party #
###############
import pytest

##########
# Module #
##########
import pedl
from conftest import message_edl, menu_edl


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


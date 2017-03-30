PEDL
=====
.. image:: https://travis-ci.org/slaclab/pedl.svg?branch=master
    :target: https://travis-ci.org/slaclab/pedl

.. image:: https://codecov.io/github/slaclab/pedl/coverage.svg?branch=master
    :target: https://codecov.io/gh/slaclab/pedl?branch=master

Python Module for Creating EDM files

Using Jinja2 templating, PEDL wraps EDM functionality into a Qt inspired API
for an intuitive module for creating screens. This abstracts much of the manual
manipulation of widgets into arbitrary combinations of layouts

Usage
=====
The main workhorse of the module is the Designer, analagous to QApplication.
The main difference is that each Designer has the main window rolled into the
object::

    import pedl
    app = pedl.Designer()


Widgets have a variety of options represented as simple attributes::

    from pedl.choices import ColorChoice
    
    go   = pedl.Rectangle(w=100, h=50, fill=ColorChoice.Green) 
    slow = pedl.Rectangle(w=100, h=50, fill=ColorChoice.Yellow) 
    stop = pedl.Rectangle(w=100, h=50, fill=ColorChoice.Red)


These can be added to the Designer indvidually or in layouts that handle the
positioning of each widget in relationship to both the screen and other widgets::
    
    from pedl.choices import AlignmentChoice

    stop_light = pedl.VBoxLayout(spacing=10, alignment=AlignmentChoice.Left)

    for light in (go, slow, stop):
        stop_light.addWidget(light)

    app.window.setLayout(stop_light)


The output can either be saved to a file, or directly viewed from the
application::

    app.exec_()

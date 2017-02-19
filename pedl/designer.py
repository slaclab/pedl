import os
import sys
from jinja2 import Environment, FileSystemLoader

from .widget import Widget

class Designer:

    def __init__(self, template_dir=None):

        self.layout  = None
        self.widgets = list()

        #Load saved templates
        if not template_dir:
            template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '../templates')

        self.env = Environment(loader=FileSystemLoader(template_dir))



    def addWidget(self, widget):
        """
        Add a free-floating widget
        """
        if not isinstance(widget, Widget):
            raise TypeError('Must supply a Widget object')
        self.widgets.append(widget)


    def setLayout(self, layout):
        """
        Set the main layout
        """
        self.layout = layout


    def render_widget(self, widget):
        """
        Render a Widget into EDM
        """
        if not isinstance(widget, Widget):
            raise TypeError('Must supply a Widget object')

        template = self.env.get_template(widget.template)
        
        return template.render(widget=widget)


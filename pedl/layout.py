from .widget import Widget

class Layout(object):

    def __init__(self, spacing=5):
        self.widgets = list()
        self.spacing = spacing

    def addWidget(self, widget):
        if not isinstance(widget, Widget):
            raise TypeError('Must be an EDM Widget')

        self.widgets.append(widget)

    def addLayout(self, layout):
        if not isinstance(layout, Layout):
            raise TypeError('Must be an EDM Layout')
        self.widgets.append(layout)



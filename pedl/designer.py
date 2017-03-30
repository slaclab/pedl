"""
The :class:`.Designer` is your main entrance point into the ``pedl`` toolkit.
For those familiar with Qt, this is analagous to your ``QApplication``
object. Behind the scenes, this is where the magic happens, each widget is
simply a container for attributes that are then rendered into templates in the
Designer. The method :meth:`.render` can be used to see this in action,
but for the large part :meth:`.save` and :meth:`exec_` will do the heavy lifting
for most applications.

For more complicated sets of widgets it is easiest to manage them in sets of
nested layouts. In the mode of operation, as opposed to adding widgets one by
one, use :meth:`.setLayout` to apply your pattern to the screen.
"""
####################
# Standard Library #
####################
import os
import sys
import logging
import tempfile

####################
#    Third Party   #
####################
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

####################
#     Package      #
####################
from .widget  import PedlObject, MainWindow, Widget
from .errors  import WidgetError
from .choices import FontChoice
from .layout  import Layout
from .utils   import Font, launch

logger = logging.getLogger(__name__)

class Designer:
    """
    Main Control class for PEDL

    Parameters
    ----------
    template_dir :str, optional
        Directory to find Jinja2 templates

    Attributes
    ----------
    widgets : list
        Ordered top-level list of widgets loaded into designer

    screen : :class:`.MainWindow`
        The final screen that will be created

    env : ``jinja2.Environment``
        Environment used to render templates
    """
    def __init__(self, template_dir=None):

        self.window  = MainWindow(parent=self)
        self.widgets = list()

        #Load saved templates
        if not template_dir:
            template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '../templates')

        if not os.path.exists(template_dir):
            raise FileNotFoundError('No such directory {}'.format(template_dir))

        logger.debug('Using {} as template directory ...'.format(template_dir))

        self.env = Environment(loader=FileSystemLoader(template_dir),
                               trim_blocks=True, lstrip_blocks=True)


    def addWidget(self, widget):
        """
        Add a free-floating widget

        Parameters
        ----------
        object : :class:`.pedl.Widget` or :class:`.pedl.layout.Layout`
            Target widget or layout
        """
        if not isinstance(widget, PedlObject):
            raise TypeError('Must supply a PEDL object')

        self.widgets.append(widget)


    def findChildren(self, _type=None, name=None):
        """
        All widgets in designer, even those in child layouts
        
        """
        widgets = []

        #Recursive widget search function
        def recursive_widget(widget):
            if isinstance(widget, Layout):
                for widget in widget.widgets:
                    recursive_widget(widget)
            elif isinstance(widget, Widget):
                widgets.append(widget)

        #Find all widgets
        for widget in self.widgets:
            recursive_widget(widget)

        #Filter by type
        if _type:
            widgets = [w for w in widgets if isinstance(w, _type)]

        #Filter by name
        if name:
            widgets = [w for w in widgets if w.name == name]

        return widgets


    def render(self, obj):
        """
        Render a ``PedlObject`` into EDM

        Parameters
        ----------
        obj : :class:`.PedlObject`
            Either a :class:`.Widget` or :class:`.Layout`

        Returns
        -------
        edl : str
            Text that will be put into the edl file
        """
        edl = []

        if isinstance(obj, Layout):
            widgets = obj.widgets

        elif isinstance(obj, PedlObject):
            widgets = [obj]

        for widget in widgets:
            if isinstance(widget, Layout):
                logger.debug('Rendering child layout ...')
                edl.append(self.render(widget))

            else:
                logger.debug('Rendering widget {} ...'.format(widget.name))
                try:
                    template = self.env.get_template(widget.template)
                    logger.debug('Using template {} ...'.format(template.filename))

                except TemplateNotFound:
                    raise WidgetError('Widget {} has non-existant template {}'
                                      ''.format(widget.name, widget.template))

                edl.append(template.render(widget=widget))

        return '\n\n'.join(edl)


    def exec_(self, wd=None, wait=True, **kwargs):
        """
        Show the current EDM screen

        Parameters
        ----------
        wd : str, optional
            Working directory to launch screen

        wait : bool, optional
            Block the main thread while the EDM preview is open

        kwargs :
            Represent macro substitutions as keyword arguments

        Returns
        -------
        proc : ``subprocess.Popen``
            Process containing EDM launch
        """
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.edl') as temp:
            self.dump(temp)
            return launch(temp.name, wd=wd, wait=wait ,**kwargs)


    def dump(self, handle):
        """
        Save the screen to a file handle

        Parameters
        ----------
        handle : file-like object
            File to store rendered created PEDL objects
        """
        if not handle.name.endswith('.edl'):
            logger.warning('Filename does not have suffix .edl ',
                           'EDM will not be able to launch this file')

        #Basic object list
        objs = [self.window]
        objs.extend(self.widgets)

        edl  = [self.render(obj) for obj in objs]

        handle.write('\n\n'.join(edl))
        handle.flush()


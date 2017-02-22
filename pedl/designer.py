import os
import sys
import logging
import tempfile
import subprocess
from distutils.spawn import find_executable

from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateNotFound

from .font    import Font
from .widget  import PedlObject, Widget
from .errors  import WidgetError
from .choices import FontChoice
from .layout  import Layout

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

    env : ``jinja2.Environment``
        Environment used to render templates
    """
    _w    = 750
    _h    = 1100
    _font = FontChoice.Helvetica

    def __init__(self, template_dir=None):

        self.widgets = list()

        #Load saved templates
        if not template_dir:
            template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '../templates')

        if not os.path.exists(template_dir):
            raise FileNotFoundError('No such directory {}'.format(template_dir))

        logger.debug('Using {} as template directory ...'.format(template_dir))

        self.env = Environment(loader=FileSystemLoader(template_dir))


    @property
    def w(self):
        """
        Width of screen
        """
        return self._w

    @w.setter
    def w(self, value):
        self._w = int(value)


    @property
    def h(self):
        """
        Height of screen
        """
        return self._h

    @h.setter
    def h(self, value):
        self._h = int(value)


    @property
    def font(self):
        """
        Set the default font for the screen
        """
        return self._font

    @font.setter
    def font(self, value):
        if isinstance(value, Font):
            value = value.font

        self._font = FontChoice(value)


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


    @property
    def all_widgets(self):
        """
        All widgets in designer, even those in child layouts
        """
        widgets = []

        #Recursive search of widget tree
        def recursive_widget(widget):
            if isinstance(widget, Layout):
                for widget in widget.widgets:
                    recursive_widget(widget)
            elif isinstance(widget, Widget):
                widgets.append(widget)

        for widget in self.widgets:
            recursive_widget(widget)

        return widgets


    def setLayout(self, layout, origin = (5,5)):
        """
        Set the main layout

        This clears the current screen and draws all of the widgets as
        described by the given layout

        Parameters
        ----------
        layout : :class:`.pedl.Layout`
            Master layout for screen

        origin : tuple, optional
            (x,y) location for the top left corner of the layout
        """
        if not isinstance(layout, Layout):
            raise TypeError('Must provide a Layout object')

        layout.x, layout.y = origin
        self.widgets = [layout]


    def render_object(self, obj):
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
        edl = ''

        if isinstance(obj, Widget):
            widgets = [widget]

        elif isinstance(obj, Layout):
            widgets = obj.widgets

        for widget in widgets:
            if isinstance(widget, Layout):
                logger.debug('Rendering child layout ...')
                edl += self.render_object(widget)

            else:
                logger.debug('Rendering widget {} ...'.format(widget.name))
                try:
                    template = self.env.get_template(widget.template)
                    logger.debug('Using template {} ...'.format(template.filename))

                except TemplateNotFound:
                    raise WidgetError('Widget {} has non-existant template {}'
                                      ''.format(widget.name, widget.template))

                edl += template.render(widget=widget)

        return edl


    def show(self, wd=None, wait=True, **kwargs):
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

        See Also
        --------
        :meth:`.Designer.launch`
        """
        with tempfile.TemporaryFile(mode='w+') as f:
            self._create(f, title='PEDL Designer')
            return self._launch(f.name, wd=wd, wait=wait ,**kwargs)


    def save(self, path, title=None):
        """
        Save the screen to an edl file

        Parameters
        ----------
        path : str
            Desired filename and path

        title: str, optional
            Title of Page
        """
        if not path.endswith('.edl'):
            path += '.edl'

        with open(path, 'w+') as f:
            self._create(f, title=title)


    def launch(self, path, wait=True, wd=None, **kwargs):
        """
        Launch an EDL file

        Parameters
        ----------
        path : str
            Path to file

        wd : str, optional
            Working directory to launch screen, otherwise the current directory
            is used

        wait : bool, optional
            Block the main thread while the EDM preview is open

        kwargs : optional
            Represent EDM macros as keyword arguments

        Returns
        -------
        proc : ``subprocess.Popen``
            Process containing EDM launch

        Raises
        ------
        FileNotFoundError:
            If the .edl file does not exist

        EnvironmentError:
            If the ``edm`` executable is not in the system path

        Example
        -------
        .. code::

            edm_proc = designer.launch('path/to/my.edl', MACRO='TST:MACRO')
        """
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        edm_args = ['edm', '-x']

        if kwargs:
            edm_args.append(','.join(['='.join([key,value])
                            for (key,value) in kwargs.items()]))

        edm_args.append(path)

        try:
            proc = subprocess.Popen(edm_args, cwd=wd, stdout=None)

            if wait:
                proc.wait()

        except OSError:
            if not find_executable('edm'):
                raise EnvironmentError('EDM is not in current environment')

            raise

        except KeyboardInterrupt:
            print('Preview aborted ...')

        return proc


    def _create(self,f, title=None):
        """
        Draw the EDL screen
        """
        screen = self.env.get_template('window.edl')
        f.write(screen.render(title, self))

        for widget in widgets:
            f.write(self.render_widget(widget))


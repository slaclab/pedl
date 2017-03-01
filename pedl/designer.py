import os
import sys
import logging
import tempfile
import subprocess
from distutils.spawn import find_executable

from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateNotFound

from .font    import Font
from .widget  import PedlObject, Screen, Widget
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
    def __init__(self, template_dir=None):

        self.screen  = Screen(parent=self)
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
        edl = []

        if isinstance(obj, Layout):
            widgets = obj.widgets

        elif isinstance(obj, PedlObject):
            widgets = [obj]

        for widget in widgets:
            if isinstance(widget, Layout):
                logger.debug('Rendering child layout ...')
                edl.append(self.render_object(widget))

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
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.edl') as temp:
            self._create(temp.file)
            return self.launch(temp.name, wd=wd, wait=wait ,**kwargs)


    def save(self, path):
        """
        Save the screen to an edl file

        Parameters
        ----------
        path : str
            Desired filename and path
        """
        if not path.endswith('.edl'):
            path += '.edl'

        with open(path, 'w+') as f:
            self._create(f)


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

        OSError:
            If the ``edm`` executable is not in the system path

        Example
        -------
        .. code::

            edm_proc = designer.launch('path/to/my.edl', MACRO='TST:MACRO')
        """
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        edm_args = ['edm', '-x', '-eolc']

        if kwargs:
            edm_args.append(','.join(['='.join([key,value])
                            for (key,value) in kwargs.items()]))

        edm_args.append(path)

        try:
            logger.debug("Launching {} with the following command {}"
                         "".format(path, edm_args))
            proc = subprocess.Popen(edm_args, cwd=wd, stdout=None)

            if wait:
                proc.wait()

        except OSError:
            if not find_executable('edm'):
                raise OSError('EDM is not in current environment')

            raise

        except KeyboardInterrupt:
            print('Preview aborted ...')
            proc.terminate()

        return proc


    def _create(self,f):
        """
        Draw the EDL screen
        """
        objs = [self.screen, *self.widgets]
        edl  = [self.render_object(obj) for obj in objs]
        f.write('\n\n'.join(edl))
        f.flush()


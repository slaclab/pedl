import versioneer
from setuptools import (setup, find_packages)


setup(name    = 'pedl',
      version  = versioneer.get_version(),
      cmdclass = versioneer.get_cmdclass(),
      license = 'BSD-like',
      author  = 'SLAC National Accelerator Laboratory',

      packages    = find_packages(),
      description = 'Qt Inspired Wrapper for creation of EDM files'

    )

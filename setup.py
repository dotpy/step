#!/usr/bin/env python


"""
This is the installation script of the step module, a light and fast template engine. You can run it by typing:

  python setup.py install

You can also run the test suite by running:

  python setup.py test
"""


import sys
from distutils.core import setup
from step.tests import TestCommand


__author__ = "Daniele Mazzocchio <danix@kernel-panic.it>"
__version__ = "0.0.3"
__date__    = "Jul 25, 2019"


# Python versions prior 2.2.3 don't support 'classifiers' and 'download_url'
if sys.version < "2.2.3":
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name             = "step-template",
      version          = __version__,
      author           = "Daniele Mazzocchio",
      author_email     = "danix@kernel-panic.it",
      packages         = ["step", "step.tests"],
      cmdclass         = {"test": TestCommand},
      description      = "Simple Template Engine for Python",
      download_url     = "https://github.com/dotpy/step/archive/step-0.0.3.tar.gz",
      classifiers      = ["Development Status :: 5 - Production/Stable",
                          "Environment :: Console",
                          "Intended Audience :: Developers",
                          "License :: OSI Approved :: BSD License",
                          "Natural Language :: English",
                          "Operating System :: OS Independent",
                          "Programming Language :: Python",
                          "Topic :: Text Processing"],
      url              = "https://github.com/dotpy/step",
      license          = "OSI-Approved :: BSD License",
      keywords         = "templates templating template-engines",
      long_description = "step is a pure-Python module providing a very "
                         "simple template engine with minimum syntax. It "
                         "supports variable expansion, flow control and "
                         "embedding of Python code.")

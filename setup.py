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
__version__ = "0.0.2"
__date__    = "Nov 18, 2013"


# Python versions prior 2.2.3 don't support 'classifiers' and 'download_url'
if sys.version < "2.2.3":
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name         = "step",
      version      = __version__,
      author       = "Daniele Mazzocchio",
      author_email = "danix@kernel-panic.it",
      packages     = ["step"],
      cmdclass     = {"test": TestCommand},
      description  = "Simple Template Engine for Python",
      classifiers  = ["Development status :: 2 - Pre-Alpha",
                      "Environment :: Console",
                      "Intended Audience :: Developers",
                      "License :: Other/Proprietary License",
                      "Natural Language :: English",
                      "Operating System :: OS Independent",
                      "Programming Language :: Python",
                      "Topic :: Text Processing"])

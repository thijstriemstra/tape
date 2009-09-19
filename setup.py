# Copyright (c) 2007-2009 The Tape Project.
# See LICENSE for details.

import os

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup, find_packages


def get_install_requirements():
    """
    Returns a list of dependancies for Tape to function correctly on the
    target platform.
    """
    install_requires = ['PyAMF>=0.5.1', 'zope.interface']

    return install_requires


keyw = """\
amf amf0 amf3 flex flash remoting rpc http flashplayer air bytearray
objectproxy arraycollection recordset actionscript"""

readme = os.path.join(os.path.dirname(__file__), 'README.txt')


setup(name = "Tape",
      version = "0.1a",
      description = "Media server for Flash",
      long_description = open(readme, 'rt').read(),
      url = "http://tape.collab.eu",
      author = "The Tape Project",
      author_email = "tape-dev@collab.eu",
      install_requires = get_install_requirements(),
      keywords = keyw,
      packages = find_packages(exclude=["*.tests"]),
      license = "LGPL License",
      platforms = ["any"],
      classifiers = [
    "Development Status :: 1 - Planning",
    "Natural Language :: English",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "License :: OSI Approved :: LGPL License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.3",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    "Topic :: Software Development :: Libraries :: Python Modules",]
)

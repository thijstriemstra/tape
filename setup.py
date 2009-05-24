# Copyright (c) 2007-2009 The Tape Project.
# See LICENSE for details.

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup, find_packages

setup(name = "Tape",
      version = "0.1",
      description = "Media server for Flash",
      url = "http://tape.collab.eu",
      packages = find_packages(exclude=["*.tests"]),
      license = "LGPL License",
      classifiers = [
	"Development Status :: 1 - Planning",
	"Natural Language :: English",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: LGPL License",
	"Operating System :: OS Independent",
	"Programming Language :: Python"]
)

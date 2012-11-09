#!/usr/bin/env python

name = "ytmpc"
package_name = "ytplay"

import versioneer
versioneer.versionfile_source = package_name+'/_version.py'
versioneer.versionfile_build = package_name+'/_version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = name+'-'
import os
import sys

#from setuptools import setup
from distutils.core import setup

description='Youtube MPlayer Controller'


setup(name=name,
	  version=versioneer.get_version(),
	  cmdclass=versioneer.get_cmdclass(),
	  description=description,
	  author='Stefan Huchler',
	  author_email='s.huchler@gmail.com',
	  url='https://github.com/spiderbit/'+name,
	  license='LICENSE',
	  long_description=open('README').read(),
	  packages = [package_name],
	  py_modules = ['versioneer'],
	  scripts=['bin/yt_curses', 'bin/ytmpc'],
	  requires = ['gdata (>=2.0.17)']
)

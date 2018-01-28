#!/usr/bin/env python3

from distutils.core import setup
from distutils import util

embypy_objs = util.convert_path('embypy/objects')
embypy_utils = util.convert_path('embypy/utils')
from embypy import __version__

with open('requirements.txt', 'r') as f:
  requirements = f.readlines()
requirements.extend(['ssl', 'json'])

setup(name='EmbyPy',
      version=__version__,
      description='Python API wrapper for emby media browser',
      author='Andriy Zasypkin',
      author_email='AndriyZasypkin@gmail.com',
      url='https://github.com/andy29485/embypy',
      package_dir = {
        'embypy': 'embypy',
        'embypy.utils': embypy_utils,
        'embypy.objects': embypy_objs
      },
      install_requires=requirements,
      packages=['embypy', 'embypy.objects', 'embypy.utils'],
)

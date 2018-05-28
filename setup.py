#!/usr/bin/env python3

from distutils.core import setup
from distutils import util

embypy_objs = util.convert_path('embypy/objects')
embypy_utils = util.convert_path('embypy/utils')

with open('requirements.txt', 'r') as f:
  requirements = f.readlines()

setup(name='EmbyPy',
      version='0.4.0.0',
      setup_requires=['setuptools-markdown'],
      long_description_markdown_filename='README.md',
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

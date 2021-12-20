#!/usr/bin/env python3

import os
from setuptools import setup, convert_path

embypy_objs = convert_path('embypy/objects')
embypy_utils = convert_path('embypy/utils')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='EmbyPy',
    version='0.6.6.4',
    author='Andriy Zasypkin',
    author_email='AndriyZasypkin@gmail.com',
    description='Python API wrapper for Emby Media Browser',
    long_description=read('README.md'),
    license='LGPLv3',
    keywords='Emby MediaBrowser API',
    url='https://pypi.org/project/EmbyPy/',
    package_dir={
      'embypy': 'embypy',
      'embypy.utils': embypy_utils,
      'embypy.objects': embypy_objs
    },
    install_requires=requirements,
    packages=['embypy', 'embypy.objects', 'embypy.utils'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Framework :: AsyncIO',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    ],
)

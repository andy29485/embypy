#!/usr/bin/env python3

"""
Emby API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Emby Rest API.
(c) 2017 Andriy Zasypkin
GPLv3, see LICENSE.txt for more details.
"""

__title__ = 'EmbyPy'
__author__ = 'Andriy Zasypkin'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2017, Andriy Zasypkin'

from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
  _dist = get_distribution('embypy')
  # Normalize case for Windows systems
  dist_loc = os.path.normcase(_dist.location)
  here = os.path.normcase(__file__)
  if not here.startswith(os.path.join(dist_loc, 'embypy')):
    # not installed, but there is another version that *is*
    raise DistributionNotFound
except DistributionNotFound:
  __version__ = 'Please install this project with setup.py'
else:
  __version__ = _dist.version

import embypy.utils
import embypy.objects
from embypy.emby import Emby


'''
Pure Python wrapper to the Yajl C library

.. data:: __version__

    Version of yajl-py

.. data:: yajl_version

    Version of the yajl library that was loaded
'''

import sys

from .yajl_common import (
    YajlException, YajlConfigError, YajlError, get_yajl_version,
)
from .yajl_parse import (
    YajlParseCancelled, YajlContentHandler, YajlParser,
)
from .yajl_gen import (
    YajlGenException, YajlGen,
)

__all__ = [
    'YajlException', 'YajlConfigError', 'YajlError',
    'YajlParseCancelled', 'YajlGenException',
    'YajlContentHandler', 'YajlParser', 'YajlGen',
]
__version__ = '2.1.1'
yajl_version = get_yajl_version()

def check_yajl_version():
    '''
    :rtype: bool

    Returns True, if the version of yajl is identical to the version of yajl-py
    otherwise displays a RuntimeWarning and returns False.
    '''
    if __version__ != yajl_version:
        import warnings
        warnings.warn(
            'Using Yajl-Py v%s with Yajl v%s. '
            'It is advised to use the same Yajl-Py and Yajl versions' %(
                __version__, yajl_version),
            RuntimeWarning, stacklevel=3)
        return False
    return True

check_yajl_version()

# monkey patch yajl, because anyjson devs are slacking off,
# and I got an issue request that I would like to help out.
# see https://bitbucket.org/runeh/anyjson/pull-requests/5/
class Wrapper(object):
  def __init__(self, wrapped):
    self.wrapped = wrapped
  def __getattr__(self, name):
    if name in ('dumps', 'loads'):
        raise ImportError('this is not py-yajl ... anyjson!')
    return getattr(self.wrapped, name)

sys.modules[__name__] = Wrapper(sys.modules[__name__])

'''
Pure Python wrapper to the Yajl C library
'''

from yajl_common import *
from yajl_parse import *
from yajl_gen import *

__version__ = '1.0.10'
yajl_version = get_yajl_version()

def check_yajl_version():
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

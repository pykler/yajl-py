'''
Common functions and members used by yajl-py (parse and gen)

.. data:: yajl

    The loaded ``ctypes.cdll`` handle to libyajl shared object. This is
    used to call any external api functions exported by yajl into libyajl.
'''

from ctypes import *

class YajlException(Exception):
    pass

class YajlConfigError(YajlException):
    pass

class YajlError(YajlException):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return self.value

def load_yajl():
    '''
    To be used internally by yajl-py to preload the yajl shared object

    :rtype: ctypes.cdll
    :returns: The yajl shared object
    :raises OSError: when libyajl cannot be loaded
    '''
    for yajlso in 'libyajl.so', 'libyajl.dylib':
        try:
            return cdll.LoadLibrary(yajlso)
        except OSError:
            pass
    raise OSError('Yajl shared object cannot be found. '
        'Please install Yajl and confirm it is on your shared lib path.')

def get_yajl_version():
    '''
    To be used internally by yajl-py to fetch yajl's version
    
    :rtype: string
    :returns: yajl's version in the format 'Major.Minor.Micro'
    '''
    v = '%0.6d' %yajl.yajl_version()
    return '%s.%s.%s' %tuple(map(int, [v[:-4], v[-4:-2], v[-2:]]))

yajl = load_yajl()

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
    for ftype in '', '.so', '.dylib':
        yajlso = 'libyajl%s' %(ftype)
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

yajl.yajl_alloc.restype = c_void_p
yajl.yajl_alloc.argtypes = [c_void_p, c_void_p, c_void_p]
yajl.yajl_config.restype = c_int
# yajl.yajl_config.argtypes = [c_void_p, c_int, ...]
yajl.yajl_free.argtypes = [c_void_p]
yajl.yajl_parse.restype = c_int
yajl.yajl_parse.argtypes = [c_void_p, c_char_p, c_size_t]
yajl.yajl_complete_parse.restype = c_int
yajl.yajl_complete_parse.argtypes = [c_void_p]
yajl.yajl_get_error.restype = c_char_p
yajl.yajl_get_error.argtypes = [c_void_p, c_int, c_char_p, c_size_t]
yajl.yajl_get_bytes_consumed.restype = c_uint
yajl.yajl_get_bytes_consumed.argtypes = [c_void_p, c_char_p]

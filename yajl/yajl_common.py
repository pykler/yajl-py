'''
Common functions and members used by yajl-py (parse and gen)

.. data:: yajl

    The loaded ``ctypes.cdll`` handle to libyajl shared object. This is
    used to call any external api functions exported by yajl into libyajl.
'''

from ctypes import (
    cdll, c_void_p, c_char_p, c_size_t, c_bool,
    c_int, c_longlong, c_double,
)

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
    fnames = ['libyajl%s' %(t) for t in ['', '.so', '.dylib']] + ['yajl.dll']

    for yajlso in fnames:
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

# Yajl Parse
yajl.yajl_alloc.restype = c_void_p
yajl.yajl_alloc.argtypes = [c_void_p, c_void_p, c_void_p]
yajl.yajl_config.restype = c_int
yajl.yajl_config.argtypes = [c_void_p, c_int]
yajl.yajl_free.argtypes = [c_void_p]
yajl.yajl_parse.restype = c_int
yajl.yajl_parse.argtypes = [c_void_p, c_char_p, c_size_t]
yajl.yajl_complete_parse.restype = c_int
yajl.yajl_complete_parse.argtypes = [c_void_p]
yajl.yajl_get_error.restype = c_char_p
yajl.yajl_get_error.argtypes = [c_void_p, c_int, c_char_p, c_size_t]
yajl.yajl_get_bytes_consumed.restype = c_size_t
yajl.yajl_get_bytes_consumed.argtypes = [c_void_p]
yajl.yajl_free_error.restype = None
yajl.yajl_free_error.argtypes = [c_void_p, c_char_p]
# Yajl Gen
yajl.yajl_gen_config.argtypes = [c_void_p, c_int]
yajl.yajl_gen_alloc.restype = c_void_p
yajl.yajl_gen_alloc_argtypes = [c_void_p]
yajl.yajl_gen_free.restype = None
yajl.yajl_gen_free.argtypes = [c_void_p]
yajl.yajl_gen_integer.argtypes = [c_void_p, c_longlong]
yajl.yajl_gen_double.argtypes = [c_void_p, c_double]
yajl.yajl_gen_number.argtypes = [c_void_p, c_char_p, c_int]
yajl.yajl_gen_string.argtypes = [c_void_p, c_char_p, c_int]
yajl.yajl_gen_null.argtypes = [c_void_p]
yajl.yajl_gen_bool.argtypes = [c_void_p, c_bool]
yajl.yajl_gen_map_open.argtypes = [c_void_p]
yajl.yajl_gen_map_close.argtypes = [c_void_p]
yajl.yajl_gen_array_open.argtypes = [c_void_p]
yajl.yajl_gen_array_close.argtypes = [c_void_p]
yajl.yajl_gen_get_buf.argtypes = [c_void_p, c_void_p, c_void_p]
yajl.yajl_gen_clear.argtypes = [c_void_p]
yajl.yajl_gen_reset.restype = None
yajl.yajl_gen_reset.argtypes = [c_void_p, c_char_p]

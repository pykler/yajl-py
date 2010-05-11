'''
Code that allows use of api/yajl_parse.h
'''

import sys
from yajl_common import *

# parser config
class yajl_parser_config(Structure):
    _fields_ = [
        ("allowComments", c_uint),
        ("checkUTF8", c_uint)
    ]

# Callback Functions
YAJL_NULL = CFUNCTYPE(c_int, c_void_p)
YAJL_BOOL = CFUNCTYPE(c_int, c_void_p, c_int)
YAJL_INT  = c_int
YAJL_DBL  = c_int
YAJL_NUM  = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_STR  = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_SDCT = CFUNCTYPE(c_int, c_void_p)
YAJL_DCTK = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_EDCT = CFUNCTYPE(c_int, c_void_p)
YAJL_SARR = CFUNCTYPE(c_int, c_void_p)
YAJL_EARR = CFUNCTYPE(c_int, c_void_p)
class yajl_callbacks(Structure):
    _fields_ = [
        ("yajl_null",           YAJL_NULL),
        ("yajl_boolean",        YAJL_BOOL),
        ("yajl_integer",        YAJL_INT ),
        ("yajl_double",         YAJL_DBL ),
        ("yajl_number",         YAJL_NUM ),
        ("yajl_string",         YAJL_STR ),
        ("yajl_start_map",      YAJL_SDCT),
        ("yajl_map_key",        YAJL_DCTK),
        ("yajl_end_map",        YAJL_EDCT),
        ("yajl_start_array",    YAJL_SARR),
        ("yajl_end_array",      YAJL_EARR),
    ]

# yajl_status
(
yajl_status_ok,
yajl_status_client_canceled,
yajl_status_insufficient_data,
yajl_status_error
) = map(c_int, range(4))

class YajlConfigError(Exception):
    pass

class YajlError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class YajlParseCancelled(YajlError):
    def __init__(self):
        self.value = 'Client Callback Cancelled Parse'

class YajlParser(object):
    '''
    A class that utilizes the Yajl C Library
    '''
    def __init__(self, c, buf_siz=65536):
        '''
        Takes a list of callback functions `c`. The functions
        need to be in order and accepting the correct number
        of parameters, they should also reutrn an int. See
        yajl doc for more info on parameters and return
        values.

        Callbacks must return an integer return code

        A callback return code of:
            - 0 will cancel the parse.
            - 1 will allow the parse to continue.
        '''
        c_funcs = (
            YAJL_NULL, YAJL_BOOL, YAJL_INT, YAJL_DBL, YAJL_NUM,
            YAJL_STR, YAJL_SDCT, YAJL_DCTK, YAJL_EDCT, YAJL_SARR,
            YAJL_EARR
        )
        if len(c) != len(c_funcs):
            raise Exception("Must Pass %d Functions."%(len(c_funcs)))
        for i in range(len(c)):
            c[i] = c_funcs[i](c[i])
        self.callbacks = yajl_callbacks(*c)
        self.buf_siz = buf_siz
        self.cfg = yajl_parser_config(1,1)

    def parse(self, f=sys.stdin, ctx=None):
        '''Function to parse a JSON stream.
        Parameters:
          `f`        : file stream to read from
          `buf_size` : size in bytes of read buffer
          `ctx`      : A ctypes pointer that will be passed to
                       all callback functions as the first param

        Raises an expception upon error or return value of 0
        from callback functions. A callback function that
        returns 0 should set internal variables to denote
        why they cancelled the parsing.
        '''
        hand = yajl.yajl_alloc( byref(self.callbacks), byref(self.cfg), ctx)
        try:
            while 1:
                fileData = f.read(self.buf_siz-1)
                if not fileData:
                    break
                stat = yajl.yajl_parse(hand, fileData, len(fileData))
                if  stat not in (yajl_status_ok.value,
                        yajl_status_insufficient_data.value):
                    if stat == yajl_status_client_canceled.value:
                        raise YajlParseCancelled()
                    else:
                        yajl.yajl_get_error.restype = c_char_p
                        error = yajl.yajl_get_error(
                            hand, 1, fileData, len(fileData))
                        raise YajlError(error)
        finally:
            yajl.yajl_free(hand)

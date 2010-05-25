'''
Code that allows use of api/yajl_gen.h
'''

from yajl_common import *

class yajl_gen_config(Structure):
    _fields_ = [
        ("beautify", c_uint),
        ("indentString", c_char_p),
    ]

(
yajl_gen_status_ok,
yajl_gen_keys_must_be_strings,
yajl_max_depth_exceeded,
yajl_gen_in_error_state,
yajl_gen_generation_complete,
yajl_gen_invalid_number,
yajl_gen_no_buf,
) = map(c_int, range(7))

class YajlGen(object):
    ''' Yajl Generator - json printing using yajl_gen '''
    def __init__(self, beautify=True, indent="  "):
        conf = yajl_gen_config(beautify, indent)
        self.g = yajl.yajl_gen_alloc(byref(conf), None)
    def __del__(self):
        yajl.yajl_gen_free(self.g)
    def yajl_gen_get_buf(self):
        l = c_uint()
        buf = POINTER(c_ubyte)()
        yajl.yajl_gen_get_buf(self.g, byref(buf), byref(l))
        try:
            return string_at(buf, l.value)
        finally:
            yajl.yajl_gen_clear(self.g)
    def yajl_gen_null(self):
        yajl.yajl_gen_null(self.g)
    def yajl_gen_bool(self, boolVal):
        yajl.yajl_gen_bool(self.g, boolVal)
    def yajl_gen_integer(self, number):
        yajl.yajl_gen_integer(self.g, number)
    def yajl_gen_double(self, number):
        yajl.yajl_gen_double(self.g, number)
    def yajl_gen_number(self, stringNum):
        '''
        parameter `stringNum` must be a string,
        otherwise use yajl_gen_double or yajl_gen_integer
        '''
        yajl.yajl_gen_number(self.g, c_char_p(stringNum), len(stringNum))
    def yajl_gen_string(self, stringVal):
        yajl.yajl_gen_string(self.g, c_char_p(stringVal), len(stringVal))
    def yajl_gen_map_open(self):
        yajl.yajl_gen_map_open(self.g)
    def yajl_gen_string(self, stringVal):
        yajl.yajl_gen_string(self.g, c_char_p(stringVal), len(stringVal))
    def yajl_gen_map_close(self):
        yajl.yajl_gen_map_close(self.g)
    def yajl_gen_array_open(self):
        yajl.yajl_gen_array_open(self.g)
    def yajl_gen_array_close(self):
        yajl.yajl_gen_array_close(self.g)

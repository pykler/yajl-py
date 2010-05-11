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

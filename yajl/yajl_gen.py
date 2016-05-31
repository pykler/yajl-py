'''
Code that allows use of api/yajl_gen.h

'''

from .yajl_common import YajlError, yajl
from ctypes import (
    POINTER, byref, string_at, c_ubyte, c_char_p,
    c_int, c_uint, c_longlong, c_double,
)

yajl_gen_status = {
    0: 'yajl_gen_status_ok',
    1: 'yajl_gen_keys_must_be_strings',
    2: 'yajl_max_depth_exceeded',
    3: 'yajl_gen_in_error_state',
    4: 'yajl_gen_generation_complete',
    5: 'yajl_gen_invalid_number',
    6: 'yajl_gen_no_buf',
    7: 'yajl_gen_invalid_string',
}
yajl_gen_status_ok = 0

(
yajl_gen_beautify,
yajl_gen_indent_string,
yajl_gen_print_callback,
yajl_gen_validate_utf8,
yajl_gen_escape_solidus,
) = map(c_int, [2**x for x in range(5)])

class YajlGenException(YajlError):
    pass

class YajlGen(object):
    '''
    Yajl Generator - json formatting using yajl_gen

    '''
    def __init__(self, **kwargs):
        '''
        :param beautify: To pretty print json (or not)
        :type beautify: bool
        :param indent: only valid when beautify=True
        :type indent: string

        .. attribute:: g

            instance of :ctype:`yajl_gen` returned by
            :cfunc:`yajl.yajl_gen_alloc`.
            This should not be used directly.
        '''
        self.g = yajl.yajl_gen_alloc(None)
        config_map = dict([
            ('beautify', yajl_gen_beautify),
            ('indent_string', yajl_gen_indent_string),
            ('print_callback', yajl_gen_print_callback),
            ('validate_utf8', yajl_gen_validate_utf8),
            ('gen_escape_solidus', yajl_gen_escape_solidus),
        ])
        for k,v in kwargs.items():
            self._yajl_gen('yajl_gen_config', config_map[k], v)

    def __del__(self):
        self._yajl_gen('yajl_gen_free')
    def yajl_gen_reset(self, sep=''):
        self._yajl_gen('yajl_gen_reset', sep)
    def _assert_retval(self, retval):
        '''
        :param retval: yajl_gen_status return code
        :type retval: int
        :raises YajlGenException: When retval is != yajl_gen_status_ok
        '''
        if retval != yajl_gen_status_ok:
            raise YajlGenException(yajl_gen_status[retval])
    def yajl_gen_get_buf(self):
        '''
        :returns: Formatted JSON
        :rtype: string

        This function may be called in a streaming fashion, i.e. you can call
        this method many times, it will retrieve what was generated since the
        last call.
        '''
        l = c_uint()
        buf = POINTER(c_ubyte)()
        self._assert_retval(
            self._yajl_gen('yajl_gen_get_buf', byref(buf), byref(l))
        )
        try:
            return string_at(buf, l.value)
        finally:
            self._yajl_gen('yajl_gen_clear')
    def _yajl_gen(self, name, *args):
        '''
        Call the underlying yajl_gen c function/method
        ``self.g`` must be already allocated
        '''
        return getattr(yajl, name)(self.g, *args)
    def _dispatch(self, name, *args):
        '''
        :param name: yajl func ``name`` to dispatch to
        :type name: string
        :param args: arguments to pass to the dispatchee
        :type args: list or tuple

        Asserts that the returned value is proper or raises the proper
        ``YajlGenException``
        '''
        self._assert_retval(
            self._yajl_gen(name, *args)
        )
    def yajl_gen_null(self):
        ''' Generate json value ``null`` '''
        self._dispatch('yajl_gen_null')
    def yajl_gen_bool(self, b):
        '''
        :param b: flag to be jsonified
        :type b: bool
        '''
        self._dispatch('yajl_gen_bool', b)
    def yajl_gen_integer(self, n):
        '''
        :param n: number to be jsonified
        :type n: int
        '''
        self._dispatch('yajl_gen_integer', c_longlong(n))
    def yajl_gen_double(self, n):
        '''
        :param n: number to be jsonified
        :type n: float
        '''
        self._dispatch('yajl_gen_double', c_double(n))
    def yajl_gen_number(self, s):
        '''
        :param s: number to be jsonified
        :type s: string

        **Note** to print floats or ints use :meth:`yajl_gen_double`
        or :meth:`yajl_gen_integer` respectively.
        '''
        self._dispatch('yajl_gen_number', c_char_p(s), len(s))
    def yajl_gen_string(self, s):
        '''
        :param s: string to be jsonified
        :type s: string
        '''
        self._dispatch('yajl_gen_string', c_char_p(s), len(s))
    def yajl_gen_map_open(self):
        ''' indicate json map begin '''
        self._dispatch('yajl_gen_map_open')
    def yajl_gen_map_close(self):
        ''' indicate json map close '''
        self._dispatch('yajl_gen_map_close')
    def yajl_gen_array_open(self):
        ''' indicate json array begin '''
        self._dispatch('yajl_gen_array_open')
    def yajl_gen_array_close(self):
        ''' indicate json array close '''
        self._dispatch('yajl_gen_array_close')

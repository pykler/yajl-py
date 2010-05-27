'''
Code that allows use of api/yajl_gen.h

'''

from yajl_common import *

yajl_gen_status = {
    0: 'yajl_gen_status_ok',
    1: 'yajl_gen_keys_must_be_strings',
    2: 'yajl_max_depth_exceeded',
    3: 'yajl_gen_in_error_state',
    4: 'yajl_gen_generation_complete',
    5: 'yajl_gen_invalid_number',
    6: 'yajl_gen_no_buf',
}
yajl_gen_status_ok = 0

class yajl_gen_config(Structure):
    _fields_ = [
        ("beautify", c_uint),
        ("indentString", c_char_p),
    ]

class YajlGenException(YajlError):
    pass

class YajlGen(object):
    '''
    Yajl Generator - json formatting using yajl_gen

    '''
    def __init__(self, beautify=True, indent="  "):
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
        conf = yajl_gen_config(beautify, indent)
        self.g = yajl.yajl_gen_alloc(byref(conf), None)
    def __del__(self):
        yajl.yajl_gen_free(self.g)
    def _assert_retval(retval):
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
            yajl.yajl_gen_get_buf(self.g, byref(buf), byref(l))
        )
        try:
            return string_at(buf, l.value)
        finally:
            yajl.yajl_gen_clear(self.g)
    def _dispatch(self, name, *args):
        '''
        :param name: yajl func ``name`` to dispatch to
        :type name: string
        :param args: arguments to pass to the dispatchee
        :type args: list or tuple
        '''
        self._assert_retval(
            getattr(yajl, name)(self.g, *args)
        )
    def yajl_gen_null(self):
        ''' Generate json value ``null`` '''
        self._dispatch('yajl_gen_null', self.g)
    def yajl_gen_bool(self, b):
        ''' 
        :param b: flag to be jsonified
        :type b: bool
        '''
        self._dispatch('yajl_gen_bool', self.g, b)
    def yajl_gen_integer(self, n):
        ''' 
        :param n: number to be jsonified
        :type n: int
        '''
        self._dispatch('yajl_gen_integer', self.g, n)
    def yajl_gen_double(self, n):
        ''' 
        :param n: number to be jsonified
        :type n: float
        '''
        self._dispatch('yajl_gen_double', self.g, n)
    def yajl_gen_number(self, s):
        '''
        :param s: number to be jsonified
        :type s: string

        **Note** to print floats or ints use :meth:`yajl_gen_double`
        or :meth:`yajl_gen_integer` respectively.
        '''
        self._dispatch('yajl_gen_number', self.g, c_char_p(s), len(s))
    def yajl_gen_string(self, s):
        ''' 
        :param s: string to be jsonified
        :type s: string
        '''
        self._dispatch('yajl_gen_string', self.g, c_char_p(s), len(s))
    def yajl_gen_map_open(self):
        ''' indicate json map begin '''
        self._dispatch('yajl_gen_map_open', self.g)
    def yajl_gen_map_close(self):
        ''' indicate json map close '''
        self._dispatch('yajl_gen_map_close', self.g)
    def yajl_gen_array_open(self):
        ''' indicate json array begin '''
        self._dispatch('yajl_gen_array_open', self.g)
    def yajl_gen_array_close(self):
        ''' indicate json array close '''
        self._dispatch('yajl_gen_array_close', self.g)

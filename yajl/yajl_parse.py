'''
Code that allows use of api/yajl_parse.h
'''

import sys
import six
from abc import ABCMeta, abstractmethod
from .yajl_common import yajl, YajlError, YajlConfigError
from ctypes import (
    Structure, CFUNCTYPE, POINTER, byref, string_at,
    c_void_p, c_char_p, c_ubyte, c_int, c_uint, c_longlong, c_double,
)

# Callback Functions
YAJL_NULL = CFUNCTYPE(c_int, c_void_p)
YAJL_BOOL = CFUNCTYPE(c_int, c_void_p, c_int)
YAJL_INT  = CFUNCTYPE(c_int, c_void_p, c_longlong)
YAJL_DBL  = CFUNCTYPE(c_int, c_void_p, c_double)
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

# yajl option
(
yajl_allow_comments,
yajl_dont_validate_strings,
yajl_allow_trailing_garbage,
yajl_allow_multiple_values,
yajl_allow_partial_values
) = map(c_int, [2**x for x in range(5)])

# yajl_status
(
yajl_status_ok,
yajl_status_client_canceled,
yajl_status_error
) = map(c_int, range(3))

class YajlParseCancelled(YajlError):
    def __init__(self):
        self.value = 'Client Callback Cancelled Parse'

class YajlContentHandler(object):
    '''
    Subclass this Abstract Base Class and implement the callback routines that
    will be called by the :class:`YajlParser` instance that you will pass an
    instance of the subclass (phew! did you get that?) to.

    Note about handling of numbers (from yajl docs):

      yajl will only convert numbers that can be represented in a double
      or a long long int.  All other numbers will be passed to the client
      in string form using the yajl_number callback.  Furthermore, if
      yajl_number is not NULL, it will always be used to return numbers,
      that is yajl_integer and yajl_double will be ignored. If
      yajl_number is NULL but one of yajl_integer or yajl_double are
      defined, parsing of a number larger than is representable
      in a double or long long int will result in a parse error.

    Due to the above, implementing :meth:`yajl_number` takes prescedence and
    the :meth:`yajl_integer` & :meth:`yajl_double` callbacks will be ignored.
    For this reason none of these three methods are enforced by the Abstract
    Base Class

    **Note** all methods must accept a param :obj:`ctx` as the first argument,
    this is a yajl feature that is implemented in yajl-py but not very useful
    in python.  see :meth:`YajlParser.parse` for more info on :obj:`ctx`.
    '''
    __metaclass__ = ABCMeta
    @abstractmethod
    def yajl_null(self, ctx):
        pass
    @abstractmethod
    def yajl_boolean(self, ctx, boolVal):
        pass
#     @abstractmethod
#     def yajl_integer(self, ctx, integerVal):
#         pass
#     @abstractmethod
#     def yajl_double(self, ctx, doubleVal):
#         pass
#     @abstractmethod
#     def yajl_number(self, ctx, stringVal):
#         pass
    @abstractmethod
    def yajl_string(self, ctx, stringVal):
        pass
    @abstractmethod
    def yajl_start_map(self, ctx):
        pass
    @abstractmethod
    def yajl_map_key(self, ctx, stringVal):
        pass
    @abstractmethod
    def yajl_end_map(self, ctx):
        pass
    @abstractmethod
    def yajl_start_array(self, ctx):
        pass
    @abstractmethod
    def yajl_end_array(self, ctx):
        pass
    def parse_start(self):
        ''' Called before each stream is parsed '''
    def parse_buf(self):
        ''' Called when a complete buffer has been parsed from the stream '''
    def complete_parse(self):
        ''' Called when the parsing of the stream has finished '''

class YajlParser(object):
    '''
    A class that utilizes the Yajl C Library
    '''
    def __init__(self, content_handler=None, buf_siz=65536, **kwargs):
        '''
        :type content_handler: :class:`YajlContentHandler`
        :param content_handler: content handler instance hosting the
            callbacks that will be called while parsing.
        :type buf_siz: int
        :param buf_siz: number of bytes to process from the input stream
            at a time (minimum 1)

        To configure the parser you need to set attributes. Attribute
        names are similar to that of yajl names less the "yajl_" prefix,
        for example:
            to enable yajl_allow_comments, set self.allow_comments=True
        '''
        # input validation
        if buf_siz <= 0:
            raise YajlConfigError('Buffer Size (buf_siz) must be set > 0')
        c_funcs = (
            YAJL_NULL, YAJL_BOOL, YAJL_INT, YAJL_DBL, YAJL_NUM,
            YAJL_STR, YAJL_SDCT, YAJL_DCTK, YAJL_EDCT, YAJL_SARR,
            YAJL_EARR
        )
        def yajl_null(ctx):
            return dispatch('yajl_null', ctx)
        def yajl_boolean(ctx, boolVal):
            return dispatch('yajl_boolean', ctx, boolVal)
        def yajl_integer(ctx, integerVal):
            return dispatch('yajl_integer', ctx, integerVal)
        def yajl_double(ctx, doubleVal):
            return dispatch('yajl_double', ctx, doubleVal)
        def yajl_number(ctx, stringVal, stringLen):
            return dispatch('yajl_number', ctx, string_at(stringVal, stringLen))
        def yajl_string(ctx, stringVal, stringLen):
            return dispatch('yajl_string', ctx, string_at(stringVal, stringLen))
        def yajl_start_map(ctx):
            return dispatch('yajl_start_map', ctx)
        def yajl_map_key(ctx, stringVal, stringLen):
            return dispatch('yajl_map_key', ctx, string_at(stringVal, stringLen))
        def yajl_end_map(ctx):
            return dispatch('yajl_end_map', ctx)
        def yajl_start_array(ctx):
            return dispatch('yajl_start_array', ctx)
        def yajl_end_array(ctx):
            return dispatch('yajl_end_array', ctx)
        def dispatch(func, *args, **kwargs):
            try:
                getattr(self.content_handler, func)(*args, **kwargs)
                return 1
            except Exception:
                self._exc_info = sys.exc_info()
                return 0

        if content_handler is None:
            self.callbacks = None
        else:
            callbacks = [
                yajl_null, yajl_boolean, yajl_integer, yajl_double,
                yajl_number, yajl_string,
                yajl_start_map, yajl_map_key, yajl_end_map,
                yajl_start_array, yajl_end_array,
            ]
            # cannot have both number and integer|double
            if hasattr(content_handler, 'yajl_number'):
                # if yajl_number is available, it takes precedence
                callbacks[2] = callbacks[3] = 0
            else:
                callbacks[4] = 0
            # cast the funcs to C-types
            callbacks = [
                c_func(callback)
                for c_func, callback in zip(c_funcs, callbacks)
            ]
            self.callbacks = byref(yajl_callbacks(*callbacks))

        # set self's vars
        self.buf_siz = buf_siz
        self.content_handler = content_handler

    def yajl_config(self, hand):
        for k,v in [
            (yajl_allow_comments, 'allow_comments'),
            (yajl_dont_validate_strings, 'dont_validate_strings'),
            (yajl_allow_comments, 'allow_comments'),
            (yajl_dont_validate_strings, 'dont_validate_strings'),
            (yajl_allow_trailing_garbage, 'allow_trailing_garbage'),
            (yajl_allow_multiple_values, 'allow_multiple_values'),
            (yajl_allow_partial_values, 'allow_partial_values'),
        ]:
            if hasattr(self, v):
                yajl.yajl_config(hand, k, getattr(self, v))

    def parse(self, f=sys.stdin, ctx=None):
        '''Function to parse a JSON stream.

        :type f: file
        :param f: stream to parse JSON from
        :type ctx: ctypes.POINTER
        :param ctx: passed to all callback functions as the first param this is
         a feature of yajl, and not very useful in yajl-py since the context is
         preserved using the content_handler instance.
        :raises YajlError: When invalid JSON in input stream found
        '''
        if f is sys.stdin and hasattr(f, 'buffer'):
            # raw binary buffer available use instead
            # needed to read bytes in python3
            f = f.buffer
        if self.content_handler:
            self.content_handler.parse_start()
        hand = yajl.yajl_alloc(self.callbacks, None, ctx)
        self.yajl_config(hand)
        try:
            while 1:
                fileData = f.read(self.buf_siz)
                if not fileData:
                    stat = yajl.yajl_complete_parse(hand)
                else:
                    stat = yajl.yajl_parse(hand, fileData, len(fileData))
                if self.content_handler:
                    self.content_handler.parse_buf()
                if  stat != yajl_status_ok.value:
                    if stat == yajl_status_client_canceled.value:
                        # it means we have an exception
                        if self._exc_info:
                            exc_info = self._exc_info
                            six.reraise(exc_info[0], exc_info[1], exc_info[2])
                        else: # for some reason we have no error stored
                            raise YajlParseCancelled()
                    else:
                        yajl.yajl_get_error.restype = c_char_p
                        error = yajl.yajl_get_error(
                            hand, 1, fileData, len(fileData))
                        # in python3 error is bytes so must be encoded
                        # to something printable
                        error = error.decode('latin-1')
                        raise YajlError(error)
                if not fileData:
                    if self.content_handler:
                        self.content_handler.complete_parse()
                    break
        finally:
            yajl.yajl_free(hand)

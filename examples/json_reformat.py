'''
Python implementation of the Yajl C json_reformat application
'''

import os
import sys
BASEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASEPATH, '%s/..' %BASEPATH] + sys.path
from yajl import __version__ as yajl_version
from yajl import *

import optparse

class ReformatContentHandler(YajlContentHandler):
    '''
    Content handler to reformat a json file using yajl_gen
    '''
    def __init__(self, beautify=True, indent="  "):
        self.out = sys.stdout
        self.conf = yajl_gen_config(beautify, indent)
    def parse_start(self):
        self.g = yajl.yajl_gen_alloc(byref(self.conf), None)
    def parse_buf(self):
        l = c_uint()
        buf = POINTER(c_ubyte)()
        yajl.yajl_gen_get_buf(self.g, byref(buf), byref(l))
        self.out.write(string_at(buf, l.value))
        yajl.yajl_gen_clear(self.g)
    def parse_complete(self):
        yajl.yajl_gen_free(self.g)
    def yajl_null(self, ctx):
        yajl.yajl_gen_null(self.g)
    def yajl_boolean(self, ctx, boolVal):
        yajl.yajl_gen_bool(self.g, boolVal)
    def yajl_number(self, ctx, stringNum):
        yajl.yajl_gen_number(self.g, c_char_p(stringNum), len(stringNum))
    def yajl_string(self, ctx, stringVal):
        yajl.yajl_gen_string(self.g, c_char_p(stringVal), len(stringVal))
    def yajl_start_map(self, ctx):
        yajl.yajl_gen_map_open(self.g)
    def yajl_map_key(self, ctx, stringVal):
        yajl.yajl_gen_string(self.g, c_char_p(stringVal), len(stringVal))
    def yajl_end_map(self, ctx):
        yajl.yajl_gen_map_close(self.g)
    def yajl_start_array(self, ctx):
        yajl.yajl_gen_array_open(self.g)
    def yajl_end_array(self, ctx):
        yajl.yajl_gen_array_close(self.g)


def main():
    opt_parser = optparse.OptionParser(
        description='reformat json from stdin',
        version='Yajl-Py for Yajl %s' %yajl_version)
    opt_parser.add_option("-m",
        dest="beautify", action="store_false", default=True,
        help="minimize json rather than beautify (default)")
    opt_parser.add_option("-u",
        dest="check_utf8", action='store_false', default=True,
        help="allow invalid UTF8 inside strings during parsing")
    (options, args) = opt_parser.parse_args()
    yajl_parser = YajlParser(
        ReformatContentHandler(beautify=options.beautify),
        check_utf8=options.check_utf8)
    yajl_parser.parse()

if __name__ == "__main__":
    main()

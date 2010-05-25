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
        self.beautify = beautify
        self.indent = indent
    def parse_start(self):
        self.g = YajlGen(beautify=self.beautify, indent=self.indent)
    def parse_buf(self):
        self.out.write(self.g.yajl_gen_get_buf())
    def parse_complete(self):
        # not necessary, gc will do this @ python shutdown
        del self.g
    def yajl_null(self, ctx):
        self.g.yajl_gen_null()
    def yajl_boolean(self, ctx, boolVal):
        self.g.yajl_gen_bool(boolVal)
    def yajl_number(self, ctx, stringNum):
        self.g.yajl_gen_number(stringNum)
    def yajl_string(self, ctx, stringVal):
        self.g.yajl_gen_string(stringVal)
    def yajl_start_map(self, ctx):
        self.g.yajl_gen_map_open()
    def yajl_map_key(self, ctx, stringVal):
        self.g.yajl_gen_string(stringVal)
    def yajl_end_map(self, ctx):
        self.g.yajl_gen_map_close()
    def yajl_start_array(self, ctx):
        self.g.yajl_gen_array_open()
    def yajl_end_array(self, ctx):
        self.g.yajl_gen_array_close()


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

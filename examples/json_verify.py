'''
Python implementation of the Yajl C json_verify application
'''

import six
import os
import sys
BASEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASEPATH, '%s/..' %BASEPATH] + sys.path
from yajl import __version__ as yajl_version
from yajl import *

import optparse

def main():
    opt_parser = optparse.OptionParser(
        description='validate json from stdin',
        version='Yajl-Py for Yajl %s' %yajl_version)
    opt_parser.add_option("-q",
        action="store_false", dest="verbose", default=True,
        help="quiet mode")
    opt_parser.add_option("-c",
        dest="allow_comments", action="store_true", default=False,
        help="allow comments")
    opt_parser.add_option("-u",
        dest="dont_validate_strings", action='store_true', default=False,
        help="allow invalid utf8 inside strings")
    (options, args) = opt_parser.parse_args()
    yajl_parser = YajlParser()
    yajl_parser.allow_comments = options.allow_comments
    yajl_parser.dont_validate_strings = options.dont_validate_strings
    retval = 0
    try:
        yajl_parser.parse()
    except YajlError as e:
        retval = 1
        if options.verbose:
            sys.stderr.write(e.value)
    if options.verbose:
        six.print_("JSON is %s" %("invalid" if retval else "valid"))
    raise SystemExit(retval)

if __name__ == "__main__":
    main()

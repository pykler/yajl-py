import os
import sys
BASEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASEPATH, '%s/..' %BASEPATH] + sys.path
from yajl import YajlContentHandler, YajlParser

# Sample callbacks, which output some debug info
# these are examples to show off the yajl parser
class ContentHandler(YajlContentHandler):
    def __init__(self):
        self.out = sys.stdout
    def yajl_null(self, ctx):
        self.out.write("null\n" )
    def yajl_boolean(self, ctx, boolVal):
        self.out.write("bool: %s\n" %('true' if boolVal else 'false'))
    def yajl_integer(self, ctx, integerVal):
        self.out.write("integer: %s\n" %integerVal)
    def yajl_double(self, ctx, doubleVal):
        self.out.write("double: %s\n" %doubleVal)
    def yajl_number(self, ctx, stringNum):
        ''' Since this is defined both integer and double callbacks are useless '''
        num = float(stringNum) if '.' in stringNum else int(stringNum)
        self.out.write("number: %s\n" %num)
    def yajl_string(self, ctx, stringVal):
        self.out.write("string: '%s'\n" %stringVal)
    def yajl_start_map(self, ctx):
        self.out.write("map open '{'\n")
    def yajl_map_key(self, ctx, stringVal):
        self.out.write("key: '%s'\n" %stringVal)
    def yajl_end_map(self, ctx):
        self.out.write("map close '}'\n")
    def yajl_start_array(self, ctx):
        self.out.write("array open '['\n")
    def yajl_end_array(self, ctx):
        self.out.write("array close ']'\n")


def main(args):
    parser = YajlParser(ContentHandler())
    parser.allow_multiple_values = True
    if args:
        for fn in args:
            f = open(fn)
            parser.parse(f=f)
            f.close()
    else:
        parser.parse()
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

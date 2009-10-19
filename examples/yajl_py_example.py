import sys; sys.path = ['.', '..'] + sys.path
from yajl import *

# Sample callbacks, which reprint invalid json
# these are examples to show off the yajl parser

def yajl_null(ctx):
    print "null"
    return 1

def yajl_boolean(ctx, boolVal):
    if boolVal:
        print "true,"
    else:
        print "false,"
    return 1

def yajl_integer(ctx, integerVal):
    print "%s,"%integerVal
    return 1

def yajl_double(ctx, doubleVal):
    print "%s,"%doubleVal
    return 1

def yajl_number(ctx, stringNum, stringLen):
    nstr = string_at(stringNum, stringLen)
    if '.' in nstr:
        num = float(nstr)
    else:
        num = int(nstr)
    print '%s(%s)'%(num,type(num))
    return 1

def yajl_string(ctx, stringVal, stringLen):
    print '"%s",'%string_at(stringVal, stringLen)
    return 1

def yajl_start_map(ctx):
    print "{"
    return 1

def yajl_map_key(ctx, stringVal, stringLen):
    print '"%s":'%string_at(stringVal, stringLen),
    return 1

def yajl_end_map(ctx):
    print "},"
    return 1

def yajl_start_array(ctx):
    print "["
    return 1

def yajl_end_array(ctx):
    print "],"
    return 1


def main(args):
    callbacks = [
        yajl_null,
        yajl_boolean,
        #yajl_integer,
        #yajl_double,
        0, #replacing integer callback with NULL
        0, #replacing double callback with NULL
        yajl_number, # cannot have this and (double or integer)
        yajl_string,
        yajl_start_map,
        yajl_map_key,
        yajl_end_map,
        yajl_start_array,
        yajl_end_array
    ]
    parser = YajlParser(callbacks)
    if args:
        for fn in args:
            f = open(fn)
            parser.parse(f=f)
            f.close()
    else:
        parser.parse()
    return 0

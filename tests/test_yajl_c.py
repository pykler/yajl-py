import six
import yajl
import os
import unittest

TESTPATH = os.path.dirname(__file__)

class YajlCTestContentHandler(yajl.YajlContentHandler):
    def __init__(self):
        self.out = six.BytesIO()
    def yajl_null(self, ctx):
        self.out.write(b"null\n" )
    def yajl_boolean(self, ctx, boolVal):
        self.out.write(six.b("bool: %s\n" %('true' if boolVal else 'false')))
    def yajl_integer(self, ctx, integerVal):
        self.out.write(six.b("integer: %s\n" %integerVal))
    def yajl_double(self, ctx, doubleVal):
        self.out.write(six.b("double: %s\n" %doubleVal))
#     def yajl_number(self, ctx, stringNum):
#         pass
    def yajl_string(self, ctx, stringVal):
        self.out.write(b"string: '" + stringVal + b"'\n")
    def yajl_start_map(self, ctx):
        self.out.write(b"map open '{'\n")
    def yajl_map_key(self, ctx, stringVal):
        self.out.write(b"key: '" + stringVal + b"'\n")
    def yajl_end_map(self, ctx):
        self.out.write(b"map close '}'\n")
    def yajl_start_array(self, ctx):
        self.out.write(b"array open '['\n")
    def yajl_end_array(self, ctx):
        self.out.write(b"array close ']'\n")

class YajlCTests(unittest.TestCase):
    '''
    Testing YAJL-PY interfaces/callbacks

    Description: Making sure yajl-py works with current installed yajl
    '''
    def setUp(self):
        self.content_handler = YajlCTestContentHandler()
        self.out = self.content_handler.out

    def assertSameAsGold(self, filename):
        with open('%s.gold' %filename, 'rb') as f:
            expected = f.read()
        # we currently do not test for memory leaks
        expected = expected.replace(b'memory leaks:\t0\n', b'')
        self.out.seek(0)
        got = self.out.read()
        self.assertEqual(expected, got)

    def resetOutput(self):
        self.out.seek(0)
        self.out.truncate()

def _make_test(filename, testname):
    def test(self):
        config_key = None
        config = lambda yp: setattr(yp, config_key, True)
        if testname.startswith('ac_'):
            config_key = 'allow_comments'
        if testname.startswith('ag_'):
            config_key = 'allow_trailing_garbage'
        if testname.startswith('am_'):
            config_key = 'allow_multiple_values'
        if testname.startswith('ap_'):
            config_key = 'allow_partial_values'
        for buf_siz in range(1, 32):
            # try out a range of buffer_sizes to stress stream parsing
            parser = yajl.YajlParser(self.content_handler, buf_siz=buf_siz)
            if config_key:
                config(parser)
            with open(filename, 'rb') as f:
                try:
                    parser.parse(f)
                except yajl.YajlError as e:
                    self.out.write(six.b('%s\n' % e.value.splitlines()[0]))
            self.assertSameAsGold(filename)
            self.resetOutput()
    return test

def _add_methods():
    dirpath = os.path.join(TESTPATH, 'cases')
    filenames = os.listdir(dirpath)
    for filename in filter(lambda x: x.endswith('.json'), filenames):
        fullname = os.path.join(dirpath, filename)
        name = filename[:-5]
        test = _make_test(fullname, name)
        setattr(YajlCTests, 'test_%s' %name, test)

_add_methods()

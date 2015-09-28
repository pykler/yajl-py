from yajl_test_lib import yajl
from minimocktest import MockTestCase
from StringIO import StringIO
import sys


class BaseContentHandler(yajl.YajlContentHandler):

    def yajl_null(self, ctx):
        pass

    def yajl_boolean(self, ctx, boolVal):
        pass

    def yajl_integer(self, ctx, integerVal):
        pass

    def yajl_double(self, ctx, doubleVal):
        pass

#     def yajl_number(self, ctx, stringNum):
#         pass

    def yajl_string(self, ctx, stringVal):
        pass

    def yajl_start_map(self, ctx):
        pass

    def yajl_map_key(self, ctx, stringVal):
        pass

    def yajl_end_map(self, ctx):
        pass

    def yajl_start_array(self, ctx):
        pass

    def yajl_end_array(self, ctx):
        pass


class YajlParserTests(MockTestCase):
    '''
    Testing :class:`YajlParser` interfaces/callbacks
    '''
    def setUp(self):
        MockTestCase.setUp(self)
        self.content_handler = BaseContentHandler()
        self.basic_json = StringIO('''{
            "a": [null, true, 1, 1.2, "Test Line: a"]
        }''')

    def test_integerAndDoubleCallbacks(self):
        self.mock('self.content_handler.yajl_integer')
        self.mock('self.content_handler.yajl_double')
        parser = yajl.YajlParser(self.content_handler)
        parser.parse(self.basic_json)
        self.assertSameTrace(
            'Called self.content_handler.yajl_integer(None, 1)\n'
            'Called self.content_handler.yajl_double(None, 1.2)\n'
        )

    def test_numberCallback(self):
        self.content_handler.yajl_number = None
        self.mock('self.content_handler.yajl_number')
        parser = yajl.YajlParser(self.content_handler)
        parser.parse(self.basic_json)
        self.assertSameTrace(
            "Called self.content_handler.yajl_number(None, '1')\n"
            "Called self.content_handler.yajl_number(None, '1.2')\n"
        )

    def test_numberCallbackUsedInsteadOfIntegerAndDouble(self):
        self.content_handler.yajl_number = None
        self.mock('self.content_handler.yajl_number')
        self.mock('self.content_handler.yajl_integer')
        self.mock('self.content_handler.yajl_double')
        parser = yajl.YajlParser(self.content_handler)
        parser.parse(self.basic_json)
        self.assertSameTrace(
            "Called self.content_handler.yajl_number(None, '1')\n"
            "Called self.content_handler.yajl_number(None, '1.2')\n"
        )

    def test_allCallbacksExceptNumber(self):
        for func in [
                'null', 'boolean', 'integer', 'double', 'string',
                'start_map', 'map_key', 'end_map',
                'start_array', 'end_array']:
            self.mock('self.content_handler.yajl_%s' % (func))
        parser = yajl.YajlParser(self.content_handler)
        parser.parse(self.basic_json)
        self.assertSameTrace(
            "Called self.content_handler.yajl_start_map(None)\n"
            "Called self.content_handler.yajl_map_key(None, 'a')\n"
            "Called self.content_handler.yajl_start_array(None)\n"
            "Called self.content_handler.yajl_null(None)\n"
            "Called self.content_handler.yajl_boolean(None, 1)\n"
            "Called self.content_handler.yajl_integer(None, 1)\n"
            "Called self.content_handler.yajl_double(None, 1.2)\n"
            "Called self.content_handler.yajl_string(None, 'Test Line: a')\n"
            "Called self.content_handler.yajl_end_array(None)\n"
            "Called self.content_handler.yajl_end_map(None)\n"
        )

    def test_largestNumberAcceptableInIntegerCallback(self):
        good_json = StringIO('[%s]' % (sys.maxint))
        bad_json = StringIO('[%s]' % (sys.maxint + 1))
        self.mock('self.content_handler.yajl_integer')
        parser = yajl.YajlParser(self.content_handler)
        parser.parse(good_json)
        self.assertSameTrace(
            "Called self.content_handler.yajl_integer(None, %s)\n" % sys.maxint
        )
        self.assertRaises(yajl.YajlError, parser.parse, bad_json)

    def test_ctxIsPassedToAllCallbacks(self):
        for func in [
                'null', 'boolean', 'integer', 'double', 'string',
                'start_map', 'map_key', 'end_map',
                'start_array', 'end_array']:
            self.mock('self.content_handler.yajl_%s' % (func))
        parser = yajl.YajlParser(self.content_handler)
        ctx = yajl.create_string_buffer('TEST')
        parser.parse(self.basic_json, ctx=yajl.byref(ctx))
        self.assertSameTrace(
            "Called self.content_handler.yajl_start_map(%(ctx)s)\n"
            "Called self.content_handler.yajl_map_key(%(ctx)s, 'a')\n"
            "Called self.content_handler.yajl_start_array(%(ctx)s)\n"
            "Called self.content_handler.yajl_null(%(ctx)s)\n"
            "Called self.content_handler.yajl_boolean(%(ctx)s, 1)\n"
            "Called self.content_handler.yajl_integer(%(ctx)s, 1)\n"
            "Called self.content_handler.yajl_double(%(ctx)s, 1.2)\n"
            "Called self.content_handler.yajl_string(%(ctx)s, 'Test Line: a')\n"
            "Called self.content_handler.yajl_end_array(%(ctx)s)\n"
            "Called self.content_handler.yajl_end_map(%(ctx)s)\n"
            % {'ctx': repr(yajl.addressof(ctx))}
        )

    def test_bufSizeLessThanOneRaisesException(self):
        for buf_siz in range(-5, 1):
            self.assertRaises(
                yajl.YajlConfigError,
                yajl.YajlParser, self.content_handler, buf_siz=buf_siz)

    def test_allowsNoCallbacks(self):
        parser = yajl.YajlParser()
        parser.parse(self.basic_json)

    def test_raisesExceptionOnInvalidJson(self):
        parser = yajl.YajlParser()
        invalid_json = StringIO('{ "a": }')
        self.assertRaises(
            yajl.YajlError,
            parser.parse, invalid_json)


class YajlGenTests(MockTestCase):
    '''
    Testing :class:`YajlGen` works as expected
    '''
    def test_YajlGen_callsYajlGenFreeWhenDone(self):
        self.mock('yajl.yajl.yajl_gen_config', tracker=None)
        self.mock('yajl.yajl.yajl_gen_alloc')
        self.mock('yajl.yajl.yajl_gen_free')
        g = yajl.YajlGen()
        del g
        self.assertSameTrace(
            'Called yajl.yajl.yajl_gen_alloc(None)\n'
            'Called yajl.yajl.yajl_gen_free(None)\n'
        )

    def _yajl_gen_sample(self, g):
        g.yajl_gen_map_open()
        g.yajl_gen_string("a")
        g.yajl_gen_array_open()
        g.yajl_gen_null()
        g.yajl_gen_bool(True)
        g.yajl_gen_integer(1)
        g.yajl_gen_double(-6.5)
        g.yajl_gen_number(str(3))
        yield g.yajl_gen_get_buf()
        g.yajl_gen_string("b")
        g.yajl_gen_array_close()
        g.yajl_gen_map_close()
        yield g.yajl_gen_get_buf()

    def test_YajlGen_streamedOutput(self):
        g = yajl.YajlGen(beautify=False)
        results = list(self._yajl_gen_sample(g))
        self.assertEqual(',"b"]}', results[1])

    def test_YajlGen_minimizeOutput(self):
        g = yajl.YajlGen(beautify=False)
        results = self._yajl_gen_sample(g)
        self.assertEqual(
            '{"a":[null,true,1,-6.5,3,"b"]}',
            ''.join(results))

    def test_YajlGen_beautifyOutput(self):
        g = yajl.YajlGen(beautify=True)
        results = self._yajl_gen_sample(g)
        self.assertEqual(
            '{\n'
            '    "a": [\n'
            '        null,\n'
            '        true,\n'
            '        1,\n'
            '        -6.5,\n'
            '        3,\n'
            '        "b"\n'
            '    ]\n'
            '}\n',
            ''.join(results))

    def test_YajlGen_indentOutput(self):
        g = yajl.YajlGen(beautify=True, indent_string="\t")
        results = self._yajl_gen_sample(g)
        self.assertEqual(
            '{\n'
            '\t"a": [\n'
            '\t\tnull,\n'
            '\t\ttrue,\n'
            '\t\t1,\n'
            '\t\t-6.5,\n'
            '\t\t3,\n'
            '\t\t"b"\n'
            '\t]\n'
            '}\n',
            ''.join(results))


class YajlCommonTests(MockTestCase):
    '''
    Testing common functions and the loading libyajl
    '''
    def test_load_yajl_raisesOSErrorIfYajlNotFound(self):
        self.mock('yajl.cdll.LoadLibrary', raises=OSError('ABCD'))
        e = None
        try:
            yajl.load_yajl()
        except OSError, e:
            pass
        self.assertTrue('Yajl shared object cannot be found.' in str(e))

    def test_get_yajl_version_correctlyParsesYajlVersion(self):
        for major in [0, 1, 3, 7]:
            for minor in [0, 1, 2, 5]:
                for micro in [0, 5, 10, 15, 20]:
                    yajl_version = major * 10000 + minor * 100 + micro
                    self.mock('yajl.yajl.yajl_version', returns=yajl_version)
                    self.assertEqual(
                        '%s.%s.%s' % (major, minor, micro),
                        yajl.get_yajl_version())

    def test_check_yajl_version_warnsOnlyWhenMismatchedVersions(self):
        self.mock('warnings.warn')
        self.mock('yajl.wrapped.__version__', mock_obj='1.1.1')
        self.mock('yajl.wrapped.yajl_version', mock_obj='1.1.1')
        self.assertTrue(yajl.check_yajl_version())
        self.assertSameTrace('')
        self.mock('yajl.wrapped.yajl_version', mock_obj='1.1.0')
        self.assertFalse(yajl.check_yajl_version())
        self.assertSameTrace(
            "Called warnings.warn("
            "'Using Yajl-Py v1.1.1 with Yajl v1.1.0. "
            "It is advised to use the same Yajl-Py and Yajl versions',"
            "<type 'exceptions.RuntimeWarning'>, stacklevel=3)"
        )

    def test_checkYajlPyAndYajlHaveSameVersion(self):
        self.assertTrue(yajl.check_yajl_version())

    def test_checkYajlPyRaisesImportErrorIfDumpsOrLoadsUsedAnyJSONHack(self):
        for attr in 'dumps', 'loads':
            try:
                getattr(yajl, attr)
            except ImportError:
                pass
            else:
                self.fail('No ImportError Raised for yajl.%s' % attr)

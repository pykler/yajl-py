from yajl_test_lib import *

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

class YajlPyTests(MockTestCase):
    '''
    Testing YAJL-PY interfaces/callbacks

    Description: Making sure yajl-py works with current installed yajl
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
            self.mock('self.content_handler.yajl_%s' %(func))
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
        good_json = StringIO('[%s]' %(sys.maxint))
        bad_json = StringIO('[%s]' %(sys.maxint + 1))
        self.mock('self.content_handler.yajl_integer')
        parser = yajl.YajlParser(self.content_handler)
        parser.parse(good_json)
        self.assertSameTrace(
            "Called self.content_handler.yajl_integer(None, %s)\n" %sys.maxint
        )
        self.failUnlessRaises(yajl.YajlError, parser.parse, bad_json)

    def test_ctxIsPassedToAllCallbacks(self):
        for func in [
            'null', 'boolean', 'integer', 'double', 'string',
            'start_map', 'map_key', 'end_map',
            'start_array', 'end_array']:
            self.mock('self.content_handler.yajl_%s' %(func))
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
            self.failUnlessRaises(
                yajl.YajlConfigError,
                yajl.YajlParser, self.content_handler, buf_siz=buf_siz)

    def test_allowsNoCallbacks(self):
        parser = yajl.YajlParser()
        parser.parse(self.basic_json)

    def test_raisesExceptionOnInvalidJson(self):
        parser = yajl.YajlParser()
        invalid_json = StringIO('{ "a": }')
        self.failUnlessRaises(
            yajl.YajlError,
            parser.parse, invalid_json)

    def test_load_yajl_raisesOSErrorIfYajlNotFound(self):
        self.mock('yajl.cdll.LoadLibrary', raises=OSError('ABCD'))
        e = None
        try:
            yajl.load_yajl()
        except OSError, e:
            pass
        self.failUnless('Yajl shared object cannot be found.' in str(e))

    def test_get_yajl_version_correctlyParsesYajlVersion(self):
        for major in [0, 1, 3, 7]:
            for minor in [0, 1, 2, 5]:
                for micro in [0, 5, 10, 15, 20]:
                    yajl_version = major * 10000 + minor * 100 + micro
                    self.mock('yajl.yajl.yajl_version', returns=yajl_version)
                    self.failUnlessEqual(
                        '%s.%s.%s' %(major, minor, micro),
                        yajl.get_yajl_version())

    def test_check_yajl_version_warnsOnlyWhenMismatchedVersions(self):
        import warnings
        self.mock('warnings.warn', [locals()])
        self.mock('yajl.__version__', mock_obj='1.1.1')
        self.mock('yajl.yajl_version', mock_obj='1.1.1')
        self.failUnless(yajl.check_yajl_version())
        self.assertSameTrace('')
        self.mock('yajl.yajl_version', mock_obj='1.1.0')
        self.failIf(yajl.check_yajl_version())
        self.assertSameTrace(
            "Called warnings.warn("
                "'Using Yajl-Py v1.1.1 with Yajl v1.1.0. "
                "It is advised to use the same Yajl-Py and Yajl versions',"
                "<type 'exceptions.RuntimeWarning'>, stacklevel=3)"
        )

    def test_checkYajlPyAndYajlHaveSameVersion(self):
        self.failUnless(yajl.check_yajl_version())

import six
import unittest
import ctypes
import mock
import yajl.yajl_common

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

class YajlParserTests(unittest.TestCase):
    '''
    Testing :class:`YajlParser` interfaces/callbacks
    '''
    def setUp(self):
        self.content_handler = BaseContentHandler()
        self.basic_json = six.BytesIO(b'''{
            "a": [null, true, 1, 1.2, "Test Line: a"]
        }''')

    def test_integerAndDoubleCallbacks(self):
        with mock.patch.multiple(self.content_handler,
            yajl_integer=mock.DEFAULT,
            yajl_double=mock.DEFAULT,
        ):
            parser = yajl.YajlParser(self.content_handler)
            parser.parse(self.basic_json)
            self.content_handler.yajl_integer.assert_called_with(None, 1)
            self.content_handler.yajl_double.assert_called_with(None, 1.2)

    def test_numberCallback(self):
        self.content_handler.yajl_number = None
        with mock.patch.object(self.content_handler, 'yajl_number'):
            parser = yajl.YajlParser(self.content_handler)
            parser.parse(self.basic_json)
            self.content_handler.yajl_number.assert_has_calls([
                mock.call(None, b'1'), mock.call(None, b'1.2')
            ])

    def test_numberCallbackUsedInsteadOfIntegerAndDouble(self):
        self.content_handler.yajl_number = None
        with mock.patch.multiple(self.content_handler,
            yajl_number=mock.DEFAULT,
            yajl_integer=mock.DEFAULT,
            yajl_double=mock.DEFAULT,
        ):
            parser = yajl.YajlParser(self.content_handler)
            parser.parse(self.basic_json)
            self.content_handler.yajl_number.assert_has_calls([
                mock.call(None, b'1'), mock.call(None, b'1.2')
            ])
            self.assertFalse(self.content_handler.yajl_integer.called)
            self.assertFalse(self.content_handler.yajl_double.called)

    def test_allCallbacksExceptNumber(self):
        with mock.patch.multiple(self.content_handler,
            **{
                'yajl_'+func: mock.DEFAULT
                for func in [
                    'null', 'boolean', 'integer', 'double', 'string',
                    'start_map', 'map_key', 'end_map',
                    'start_array', 'end_array'
                ]
            }
        ):
            parser = yajl.YajlParser(self.content_handler)
            parser.parse(self.basic_json)
            self.content_handler.yajl_start_map.assert_called_with(None)
            self.content_handler.yajl_map_key.assert_called_with(None, b'a')
            self.content_handler.yajl_start_array.assert_called_with(None)
            self.content_handler.yajl_null.assert_called_with(None)
            self.content_handler.yajl_boolean.assert_called_with(None, 1)
            self.content_handler.yajl_integer.assert_called_with(None, 1)
            self.content_handler.yajl_double.assert_called_with(None, 1.2)
            self.content_handler.yajl_end_array.assert_called_with(None)
            self.content_handler.yajl_end_map.assert_called_with(None)
            self.content_handler.yajl_string.assert_called_with(
                None, b'Test Line: a'
            )

    def test_largestNumberAcceptableInIntegerCallback(self):
        good_json = six.BytesIO(six.b('[%s]' %(six.MAXSIZE)))
        bad_json = six.BytesIO(six.b('[%s]' %(six.MAXSIZE+1)))
        with mock.patch.object(self.content_handler, 'yajl_integer'):
            parser = yajl.YajlParser(self.content_handler)
            parser.parse(good_json)
            self.content_handler.yajl_integer.assert_called_with(None, six.MAXSIZE)
            self.assertRaises(yajl.YajlError, parser.parse, bad_json)

    def test_ctxIsPassedToAllCallbacks(self):
        with mock.patch.multiple(self.content_handler,
            **{
                'yajl_'+func: mock.DEFAULT
                for func in [
                    'null', 'boolean', 'integer', 'double', 'string',
                    'start_map', 'map_key', 'end_map',
                    'start_array', 'end_array'
                ]
            }
        ):
            parser = yajl.YajlParser(self.content_handler)
            ctx = ctypes.create_string_buffer(b'TEST')
            parser.parse(self.basic_json, ctx=ctypes.byref(ctx))
            ctx_ref = ctypes.addressof(ctx)
            self.content_handler.yajl_start_map(ctx_ref)
            self.content_handler.yajl_map_key(ctx_ref, 'a')
            self.content_handler.yajl_start_array(ctx_ref)
            self.content_handler.yajl_null(ctx_ref)
            self.content_handler.yajl_boolean(ctx_ref, 1)
            self.content_handler.yajl_integer(ctx_ref, 1)
            self.content_handler.yajl_double(ctx_ref, 1.2)
            self.content_handler.yajl_string(ctx_ref, 'Test Line: a')
            self.content_handler.yajl_end_array(ctx_ref)
            self.content_handler.yajl_end_map(ctx_ref)

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
        invalid_json = six.BytesIO(b'{ "a": }')
        self.assertRaises(yajl.YajlError, parser.parse, invalid_json)

class YajlGenTests(unittest.TestCase):
    '''
    Testing :class:`YajlGen` works as expected
    '''
    def test_YajlGen_callsYajlGenFreeWhenDone(self):
        with mock.patch.multiple(yajl.yajl_common.yajl,
            yajl_gen_config = mock.DEFAULT,
            yajl_gen_alloc = mock.DEFAULT,
            yajl_gen_free = mock.DEFAULT,
        ):
            g = yajl.YajlGen()
            del g
            self.assertTrue(yajl.yajl_common.yajl.yajl_gen_alloc.called)
            self.assertTrue(yajl.yajl_common.yajl.yajl_gen_free.called)

    def _yajl_gen_sample(self, g):
        g.yajl_gen_map_open()
        g.yajl_gen_string(b"a")
        g.yajl_gen_array_open()
        g.yajl_gen_null()
        g.yajl_gen_bool(True)
        g.yajl_gen_integer(1)
        g.yajl_gen_double(-6.5)
        g.yajl_gen_number(b'3')
        yield g.yajl_gen_get_buf()
        g.yajl_gen_string(b'b')
        g.yajl_gen_array_close()
        g.yajl_gen_map_close()
        yield g.yajl_gen_get_buf()

    def test_YajlGen_streamedOutput(self):
        g = yajl.YajlGen(beautify=False)
        results = list(self._yajl_gen_sample(g))
        self.assertEqual(b',"b"]}', results[1])

    def test_YajlGen_minimizeOutput(self):
        g = yajl.YajlGen(beautify=False)
        results = self._yajl_gen_sample(g)
        self.assertEqual(
            b'{"a":[null,true,1,-6.5,3,"b"]}',
            b''.join(results))

    def test_YajlGen_beautifyOutput(self):
        g = yajl.YajlGen(beautify=True)
        results = self._yajl_gen_sample(g)
        self.assertEqual(
            b'{\n'
            b'    "a": [\n'
            b'        null,\n'
            b'        true,\n'
            b'        1,\n'
            b'        -6.5,\n'
            b'        3,\n'
            b'        "b"\n'
            b'    ]\n'
            b'}\n',
            b''.join(results))

    def test_YajlGen_indentOutput(self):
        g = yajl.YajlGen(beautify=True, indent_string=b"\t")
        results = self._yajl_gen_sample(g)
        self.assertEqual(
            b'{\n'
            b'\t"a": [\n'
            b'\t\tnull,\n'
            b'\t\ttrue,\n'
            b'\t\t1,\n'
            b'\t\t-6.5,\n'
            b'\t\t3,\n'
            b'\t\t"b"\n'
            b'\t]\n'
            b'}\n',
            b''.join(results))

class YajlCommonTests(unittest.TestCase):
    '''
    Testing common functions and the loading libyajl
    '''
    def test_load_yajl_raisesOSErrorIfYajlNotFound(self):
        with mock.patch.object(
            yajl.yajl_common.cdll, 'LoadLibrary',
            side_effect=OSError('ABCD'),
        ):
            error = ''
            try:
                yajl.yajl_common.load_yajl()
            except OSError as e:
                error = str(e)
            self.assertIn('Yajl shared object cannot be found.', error)

    def test_get_yajl_version_correctlyParsesYajlVersion(self):
        for major in [0, 1, 3, 7]:
            for minor in [0, 1, 2, 5]:
                for micro in [0, 5, 10, 15, 20]:
                    yajl_version = major * 10000 + minor * 100 + micro
                    with mock.patch.object(yajl.yajl_common.yajl,
                        'yajl_version',
                        side_effect=lambda *args: yajl_version,
                    ):
                        self.assertEqual(
                            '%s.%s.%s' %(major, minor, micro),
                            yajl.get_yajl_version())

    def test_check_yajl_version_warnsOnlyWhenMismatchedVersions(self):
        with mock.patch('warnings.warn') as warn:
            with mock.patch.multiple(yajl.wrapped,
                __version__='1.1.1',
                yajl_version='1.1.2', # major and minor version matching
            ):
                self.assertTrue(yajl.check_yajl_version())
                self.assertFalse(warn.called)
            with mock.patch.multiple(yajl.wrapped,
                __version__='1.1.1',
                yajl_version='1.0.0',
            ):
                self.assertFalse(yajl.check_yajl_version())
                warn.assert_called_with(
                    "Using Yajl-Py v1.1.1 with Yajl v1.0.0. It is advised "
                    "to use the same Yajl-Py and Yajl versions",
                    RuntimeWarning, stacklevel=3
                )

    def test_checkYajlPyAndYajlHaveSameVersion(self):
        self.assertTrue(yajl.check_yajl_version())

    def test_checkYajlPyRaisesImportErrorIfDumpsOrLoadsUsedAnyJSONHack(self):
        for attr in 'dumps', 'loads':
            self.assertRaises(ImportError, getattr, yajl, attr)

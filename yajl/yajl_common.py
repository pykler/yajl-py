from ctypes import *

def load_yajl():
    global yajl
    for yajlso in 'libyajl.so', 'libyajl.dylib':
        try:
            yajl = cdll.LoadLibrary(yajlso)
        except OSError:
            pass
        else:
            break
    else:
        raise OSError('Yajl shared object cannot be found. '
            'Please install Yajl and confirm it is on your shared lib path.')

def get_yajl_version():
    v = '%0.6d' %yajl.yajl_version()
    return '%s.%s.%s' %tuple(map(int, [v[:-4], v[-4:-2], v[-2:]]))

load_yajl()

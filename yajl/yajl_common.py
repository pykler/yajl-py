from ctypes import *

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


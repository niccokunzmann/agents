import sys

from streamRegister import *

try:
    import _StreamFactory as _StreamFactory
except ImportError:
    try:
        import stream._StreamFactory as _StreamFactory
    except ImportError:
        import distobj.stream._StreamFactory as _StreamFactory

import distobj
import distobj.stream

sys.modules.setdefault('StreamFactory', _StreamFactory)
sys.modules.setdefault('stream.StreamFactory', _StreamFactory)
sys.modules.setdefault('distobj.stream.StreamFactory', _StreamFactory)

locals().update(vars(_StreamFactory))


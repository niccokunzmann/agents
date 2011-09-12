import sys

try:
    import _StreamFactory as StreamFactory
except ImportError:
    try:
        import stream._StreamFactory as StreamFactory
    except ImportError:
        import distobj.stream._StreamFactory as StreamFactory

locals().update(vars(StreamFactory))

import distobj
import distobj.stream

sys.modules.setdefault('StreamFactory', StreamFactory)
sys.modules.setdefault('stream.StreamFactory', StreamFactory)
sys.modules.setdefault('distobj.stream.StreamFactory', StreamFactory)


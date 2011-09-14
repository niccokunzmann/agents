
from Stream import *

from BrokenStream import BrokenStream
import StreamFactory


class NotConnectedError(BrokenStreamError):
    pass

_l = list()

class Connection(Stream):
    
    def __init__(self, stream = None):
        self._connected = False
        if stream is None:
            stream = BrokenStream()
        self.stream = stream

    def connect(self):
        raise NotConnectedError('donnot know what to connect to')

    def isConnected(self):
        return self._connected

    def connectTo(self, stream):
        Stream.__init__(self, stream)
        self._connected = True

    def read(self, count = _l):
        if self._connected:
            if count is _l:
                return self.stream.read()
            return self.stream.read(count)
        raise NotConnectedError('the connection must be connected for reading')

    def write(self, obj):
        if self._connected:
            return self.stream.write(obj)
        raise NotConnectedError('the connection must be connected for writing')

    def update(self):
        if self._connected:
            return self.stream.update()
        raise NotConnectedError('the connection must be connected for updating')
        
    def flush(self):
        if self._connected:
            return self.stream.flush()
        raise NotConnectedError('the connection must be connected for flushing')

    def close(self):
        '''close the connection
the underlying connection is closed, too
use disconnect() to leave the underlying connection untouched
'''
        if self._connected:
            stream = self.stream
            b = BrokenStream()
            b.close()
            self.connect(b)
            if hasattr(stream, 'close'):
                stream.close()#on error the connection is already disconnected
        else:
            raise NotConnectedError('the connection must be connected for updating')

    def disconnect(self):
        '''make the connection not connected
this the default state
'''
        self._connected = False
        self.stream = BrokenStream()

def _constructor(stream, connected):
    '''constructor for StreamFactory'''
    con = Connection(stream)
    if connected:
        con.connectTo(stream)
    return con

StreamFactory.registerStream(Connection, None, \
                             lambda con: (con.stream, com.isConnected()), \
                             _constructor)


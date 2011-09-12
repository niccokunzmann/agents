
from Stream import Stream, BrokenStreamError
from distobj.objects.GlobalObject import *

from BrokenStream import BrokenStream

import thread

class NotConnectedError(BrokenStreamError):
    pass

_l = list()

class Manager(GlobalObject, Stream):
    '''A Manager is both - a stream and a special Object'''

    def __init__(self, name):
        self.default._connected = False
        self.default.stream = BrokenStream()

    def connect(self, stream):
        Stream.__init__(self, stream)
        self._connected = True

    def read(self, count = _l):
        if self._connected:
            if count is _l:
                return self.stream.read()
            return self.stream.read(count)
        raise NotConnectedError('the Manager must be connected for reading')

    def write(self, obj):
        if self._connected:
            return self.stream.write(obj)
        raise NotConnectedError('the Manager must be connected for writing')

    def update(self):
        if self._connected:
            return self.stream.update()
        raise NotConnectedError('the Manager must be connected for updating')
        
    def flush(self):
        if self._connected:
            return self.stream.flush()
        raise NotConnectedError('the Manager must be connected for flushing')

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
                stream.close()#on error the manager is already disconnected
        else:
            raise NotConnectedError('the Manager must be connected for updating')

    def disconnect(self):
        '''make the manager not connected
this the default state
'''
        self._connected = False
        self.stream = BrokenStream()

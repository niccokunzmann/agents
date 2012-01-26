
class StreamError(Exception):
    '''Base Error for Stream exceptions'''
    pass

class BrokenStreamError(EOFError, StreamError):
    '''this Error shall be raised if the Stream has stopped working'''
    pass

class StreamClosedError(BrokenStreamError):
    pass

class Stream(object):

    def __init__(self, stream):
        self.stream = stream

    def read(self, count = 0):
        self._raiseNotImplementd('read')

    def update(self):
        '''update the stream for reading'''
        self._raiseNotImplementd('update')
       
    def write(self, obj):
        self._raiseNotImplementd('write')

    def flush(self):
        '''flush the stream after writing'''
        self._raiseNotImplementd('flush')

    def close(self):
        '''close the stream'''
        self._raiseNotImplementd('close')

    def _overtake_attribute(self, attr):
        if hasattr(self.stream, attr):
            setattr(self, attr, getattr(self.stream, attr))

    def _raiseNotImplementd(self, method):
        raise NotImplementedError('%s is not implemented for %s objects' % \
                                  (method, self.getStreamClassName()))
    
    @classmethod
    def getStreamClassName(cls):
        return cls.__module__ + '__' + cls.__name__

    def fileno(self):
        '''return the fileno() of the underlying stream'''
        return self.stream.fileno()


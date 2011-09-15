
class StreamError(Exception):
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
        raise NotImplementedError('read is not implemented')
        
    def update(self):
        '''update the stream for reading'''
        raise NotImplementedError('update is not implemented')
       

    def write(self, obj):
        raise NotImplementedError('write is not implemented')

    def flush(self):
        '''flush the stream after writing'''
        raise NotImplementedError('flush is not implemented')

    def _overtake_attribute(self, attr):
        if hasattr(self.stream, attr):
            setattr(self, attr, getattr(self.stream, attr))

    @classmethod
    def getStreamClassName(cls):
        return cls.__module__ + '__' + cls.__name__

    def fileno(self):
        '''return the fileno() of the underlying stream'''
        return self.stream.fileno()

    def close(self):
        '''close the stream'''
        raise NotImplementedError('close  is not implemented')

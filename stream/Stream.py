
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
        raise NotImplementedError('update is not implemented')
       

    def write(self, obj):
        raise NotImplementedError('write is not implemented')

    def flush(self):
        raise NotImplementedError('flush is not implemented')

    def _overtake_attribute(self, attr):
        if hasattr(self.stream, attr):
            setattr(self, attr, getattr(self.stream, attr))

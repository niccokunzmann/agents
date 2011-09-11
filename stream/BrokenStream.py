from Stream import *



class BrokenStream(Stream):
    '''This Stream always simulates to be broken
if you close it the error will be changed
all methods throw an error except close

'''

    def __init__(self, stream = None):
        Stream.__init__(self, stream)
        self.error = BrokenStreamError('the stream is broken')

    def read(self, count = _l):
        '''throw BrokenStreamError or StreamClosedError if closed'''
        raise self.error
        
    def write(self, obj):
        '''throw BrokenStreamError or StreamClosedError if closed'''
        raise self.error

    def update(self):
        '''throw BrokenStreamError or StreamClosedError if closed'''
        raise self.error
        
    def flush(self):
        '''throw BrokenStreamError or StreamClosedError if closed'''
        raise self.error

    def readline(self):
        '''throw BrokenStreamError or StreamClosedError if closed'''
        self.read()

    def readlines(self):
        '''throw BrokenStreamError or StreamClosedError if closed'''
        self.readline()

    def close(self):
        '''close the stream'''
        self.error = StreamClosedError('the stream is closed')

    
import StreamFactory
StreamFactory.registerStream(BrokenStream, toTuple = StreamFactory.noArguments)


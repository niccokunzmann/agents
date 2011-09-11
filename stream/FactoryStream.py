
from Stream import *
from FileStream import FileStream


class MethodNotFound(ValueError, StreamError):
    '''the requred method was not found by the stream factory'''
    pass

class FactoryStream(Stream):

    def __init__(self, stream):
        assert hasattr(stream, 'readline'), 'readline required, '\
                                            'eventually use FileStream'
        Stream.__init__(self)

    def getFactoryStream(self):
        return self.stream

    def read(self, count = None):
        '''read a stream
count will be ignored'''
        methodname = self.stream.readline().strip()
        return self.callReadMethod(methodname)

    def callReadMethod(self, name):
        '''call the given method by name'''
        method = self.findReadMethod(name)
        try:
            if method is not None:
                return method(self.getFactoryStream())
            raise MethodNotFound('method %r was not found' % name)
        finally:
            self.cleanupRead()

    def findReadMethod(self, name):
        '''find the method by name starting with read_'''
        return getattr(self, 'read_' + name, None)

    def cleanupRead(self):
        '''throw away all remaining string'''
        self.stream.read()

    def write(self, stream):
        '''write a stream to this stream'''
        method = self.findMethod(stream)
        method(self.getFactoryStream(), stream)

    def findMethod(self, stream):
        return getattr(self, 'write_' + self.getStreamName(stream), None)

    def getStreamName(self, stream):
        return type(stream).__name__
        

        

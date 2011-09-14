
from Stream import *
from FileStream import FileStream


class MethodNotFound(ValueError, StreamError):
    '''the requred method was not found by the stream factory'''
    pass

class FactoryStream(Stream):

    def __init__(self, stream):
        assert hasattr(stream, 'readline'), 'readline required, '\
                                            'eventually use FileStream'
        Stream.__init__(self, stream)
        self._overtake_attribute('flush')

    def getFactoryStream(self):
        return self.stream

    def read(self, count = -1):
        '''read a stream'''
        l = []
        while not (len(l) >= count > -1):
            methodname = self.stream.readline().strip()
            if not methodname:
                break
            stream = self.callReadMethod(methodname)
            l.append(stream)
        return l

    def callReadMethod(self, name):
        '''call the given method by name'''
        method = self.findReadMethod(name)
        if method is not None:
            return method(self.getFactoryStream())
        raise MethodNotFound('method %r was not found' % name)
            
    def update(self):
        self.cleanupRead()
        self.stream.update()

    def findReadMethod(self, name):
        '''find the method by name starting with read_'''
        return getattr(self, 'read_' + name, None)

    def cleanupRead(self):
        '''throw away all remaining string'''
        self.stream.read()

    def write(self, obj):
        '''write a stream to this stream'''
        method = self.findWriteMethod(obj)
        method(self.getFactoryStream(), obj)

    def findWriteMethod(self, obj):
        return getattr(self, self.getWriteMethodName(obj), \
                             self.writeMethodNotFound)

    def getWriteMethodName(self, obj):
        return 'write_' + type(obj).__name__
    
    def writeMethodNotFound(self, obj):
        raise MethodNotFound('no method found to serialize %r' % obj)
        

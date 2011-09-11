
        
from FactoryStream import FactoryStream, MethodNotFound

import stringtuple

def emptyArguments(stream, *args):
    '''the stream will be initilized without any additional arguments'''
    return ()

def streamArguments(stream, *args):
    '''the stream will be initilized with its stream as argument'''
    return (stream.stream,)

class StreamFactory(FactoryStream):

    def getFactoryStream(self):
        return FactoryReader(self.stream, self)

    def registerStream(self, streamCls, name = None, toTuple = streamArguments,
                       constructor = None):
        '''register a stream to read and write'''
        if streamCls in streamRegister:
            return self.registerStream(streamRegister[streamCls])
        if type(streamCls) is tuple:
            return self.registerStream(*streamCls)
        if name is None:
            clsname = streamCls.__name__
            modname = streamCls.__module__
            if modname == clsname:
                name = modname
            else:
                name = modname + '.' + clsname
        name = name.strip().replace('\n', '\r')
        if constructor is None:
            constructor = streamCls
        streamCls.__name = name
        setattr(self, 'read_' + name, \
                self.newStreamConstructor(stream, name, constructor))
        setattr(self, 'write_' + name, \
                self.newStreamSaver(stream, name, toTuple))


    @staticmethod
    def newStreamConstructor(streamCls, name, const):
        def constructor(streamFactory):
            t = streamFactory.readTuple(stream)
            return const(*t)
        constructor.__name__ = 'contructor_' + name.replace('.', '_')
        return constructor

    @staticmethod
    def newStreamSaver(stream, name, toTuple)
        def saver(stream, obj):
            t = toTuple(obj)
            if type(t) is not tuple:
                t = (t,)
            stream.write(name + '\n')
            writeStringTuple(stream, t)
        saver.__name__ = 'saver_' + name.replace('.', '_')
        return saver



class FactoryReader(Stream):

    def __init__(self, stream, factory):
        Stream.__init__(self, stream)
        self.factory = factory

    def read(self, count = None):
        '''read a tuple, string or stream'''
        t = self.stream.read(1)
        method = getattr(self, 'read_' + t, None)
        if method is not None:
            return method()
        raise MethodNotFound(t)

    def read_t(self):
        length = int(self.stream.readline())
        return tuple([self.read() for i in xrange(length)])

    def read_s(self):
        return stringtuple.readString(self.stream)

    def read_i(self):
        return int(self.stream.readline())

    def read_a(self):
        return self.factory.read()

    def write(self, obj):
        return getattr(self, 'write_' + type(obj).__name__, self.writeAll)(obj)

    def write_str(self, obj):
        self.stream.write('s')
        stringtuple.writeString(self.stream, obj)

    def write_int(self, obj):
        self.stream.write('i')
        self.stream.write(str(obj))

    write_long = write_int

    def write_tuple(self, t):
        self.stream.write(str(len(t)) + '\n')
        for e in t:
            self.write(e)

    def writeAll(self, obj):
        self.stream.write('a')
        self.factory.write(obj)
        

streamRegister = {}

def registerStream(streamCls, name = None, \
                   toTuple = streamArguments, constructor = None):
    '''registerStream(stream, [name, [toTuple, [constructor]]])
toTuple(stream) generates a tuple of string, int, stream, tuple of stream
constructor takes the stream class and the unfolded tuple as arguments
the constructor defaults to the stream class
toTuple can be emptyArguments or streamArguments or other
'''
    streamRegister[streamCls] = (streamCls, name, toTuple, constructor)













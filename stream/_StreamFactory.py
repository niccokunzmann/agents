
from Stream import Stream
from FactoryStream import FactoryStream, MethodNotFound

import stringtuple

def noArguments(stream, *args):
    '''the stream will be initilized without any additional arguments'''
    return ()

def streamArguments(stream, *args):
    '''the stream will be initilized with its stream as argument'''
    return (stream.stream,)

class StreamNotRegistered(MethodNotFound):
    '''if the stream is not registered to serialize or desereialize
this error will be raised'''
    pass

class StreamFactory(FactoryStream):
    '''reader and writer factory for strings
the factory must be costomized to use.
register stream classes with
registerStream(stream_cls, ...)
if the stream class not known a 

'''

    def __init__(self, stream):
        '''create a reader and writer for streams around
a the given string stream
'''
        FactoryStream.__init__(self, stream)
        self._overtake_attribute('flush')
        self._overtake_attribute('update')
        self._streamClasses = []

    def getFactoryStream(self):
        '''return a Reader for other data than streams'''
        return FactoryReader(self.stream, self)

    def registerStream(self, streamCls):
        '''register a stream to be written and read
see the module function registerStream(...) for further information
streamCls should be a stream class of the name string of
a stream registered by registerStream(...) (module).
if you want to register a new stream like you do with registerStream(...)
of the module then use registerNewStream(...)
'''
        if streamCls in streamRegister:
            return self.registerNewStream(*streamRegister[streamCls])
        raise StreamNotRegistered('the stream class could not be found')
    
    def registerNewStream(self, streamCls, name, toTuple, constructor):
        '''this works like the module function registerStream()
but only for this StreamFactory

'''
        if type(streamCls) is tuple:
            return self.registerNewStream(*streamCls)
        if name is None:
            if not self.isValidStream(streamCls):
                raise ValueError('the stream class must be a Stream '\
                                 'or have a getStreamClassName() method')
            name = streamCls.getStreamClassName()
        name = name.strip().replace('\n', '\r')
        if constructor is None:
            constructor = streamCls
        streamCls.__name = name
        setattr(self, 'read_' + name, \
                self.newStreamConstructor(streamCls, name, constructor))
        setattr(self, 'write_' + name, \
                self.newStreamSaver(streamCls, name, toTuple))
        self._streamClasses.append(streamCls)


    @staticmethod
    def newStreamConstructor(streamCls, name, const):
        '''return a constructor function
that creates a stream reading information from the streamFactory
constructor(serializer)'''
        def constructor(serializer):
            t = serializer.read_tuple()
            return const(*t)
        constructor.__name__ = 'contructor_' + name.replace('.', '_')
        return constructor

    @staticmethod
    def newStreamSaver(streamCls, name, toTuple):
        '''return a saver(stream, obj) function
the saver writes the object to the stream'''
        def saver(serializer, obj):
            t = toTuple(obj)
            if type(t) is not tuple:
                t = (t,)
            serializer.stream.write(name + '\n')
            serializer.write_tuple(t)
        saver.__name__ = 'saver_' + name.replace('.', '_')
        return saver

    def getWriteMethodName(self, stream):
        '''return the method name for the stream'''
        if self.isValidStream(stream):
            return 'write_' + stream.getStreamClassName()
        return 'writeMethodNotFound'
        
    def writeMethodNotFound(self, factory, obj):
        '''raise the apropriate error for the object that should be serialized'''
        if isinstance(obj, Stream):
            raise StreamNotRegistered('stream %s not registered '\
                                      '-> cannot serialize %r' % \
                                      (type(obj).__name__, obj))
        raise MethodNotFound('no method found to serialize %r' % obj)
        

    def isValidStream(sefl, obj):
        '''=> bool wether the given obj is a valid stream object
instances and classes are tested'''
        return hasattr(obj, 'getStreamClassName')


class FactoryReader(Stream):
    '''This class is a Helper for the StreamFactory to read and write other
datatypes
supported:
    int, str, long, tuple of supported

'''
    def __init__(self, stream, factory):
        Stream.__init__(self, stream)
        self.factory = factory

    def read(self, count = None):
        '''read a tuple, string or stream'''
        t = self.stream.read(1)
        method = getattr(self, 'read_' + t, None)
        if method is not None:
            return method()
        raise MethodNotFound(repr(t))

    def read_t(self):
        'read tuple'
        length = int(self.stream.readline())
        return tuple([self.read() for i in xrange(length)])

    read_tuple = read_t

    def read_s(self):
        'read string'
        return stringtuple.readString(self.stream)
    read_str = read_s

    def read_i(self):
        'read integer'
        return int(self.stream.readline())
    read_int = read_long = read_i

    def read_a(self):
        'read all - let the factory do the work'
        return self.factory.read()

    def write(self, obj):
        'write an object'
        return getattr(self, 'write_' + type(obj).__name__, self.writeAll)(obj)

    def write_str(self, obj):
        'write a string'
        self.stream.write('s')
        stringtuple.writeString(self.stream, obj)

    def write_int(self, obj):
        'write an integer or long'
        self.stream.write('i')
        self.stream.write(str(obj) + '\n')

    write_long = write_int

    def write_tuple(self, t):
        'write a tuple'
        self.stream.write(str(len(t)) + '\n')
        for e in t:
            self.write(e)

    def writeAll(self, obj):
        'write all other - let the factory do the work'
        self.stream.write('a')
        self.factory.write(obj)
        

streamRegister = {}

def registerStream(streamCls, name = None, \
                   toTuple = streamArguments, constructor = None):
    '''registerStream(stream, [name, [toTuple, [constructor]]])
toTuple(stream) generates a tuple of string, int, stream, tuple of stream
constructor takes the stream class and the unfolded tuple as arguments
the constructor defaults to the stream class
toTuple can be noArguments or streamArguments or other
valid names for the stream are:
    <module name>.<class name>
    <class name>
    <class.getStreamClassName()>
and can be passed to StreamFactory.registerStream
'''
    t = (streamCls, name, toTuple, constructor)
    streamRegister[streamCls] = t
    streamRegister[streamCls.__name__] = t
    streamRegister[streamCls.__module__ + '.' + streamCls.__name__] = t
    streamRegister[streamCls.getStreamClassName()] = t
    

def _constructFactory(cls, stream, streams):
    fact = cls(stream)
    name = factory.__name__
    for stream in streams:
        if stream == name:
            fact.registerStream(cls)
        else:
            fact.registerStream(stream)
    return fact

def toTuple(fact):
    # todo
    return []








''' This module gathers information on how stream classes can be serialized safely

'''

def noArguments(stream, *args):
    '''the stream will be initilized without any additional arguments'''
    return ()

def streamArguments(stream, *args):
    '''the stream will be initilized with its stream as argument'''
    return (stream.stream,)

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
    

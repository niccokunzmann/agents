
from Stream import *

import sys
import time

import StringStream
import FileStream

import socket

class StreamWrap(Stream):
    def __init__(self, *args, **kw):
        d = self.getAttributes(*args, **kw)
        self.__dict__.update(d)
        self.self = None
        del self.self

    def getAttributes(self, stream, read, write):
        return locals()

    def update(self):
        pass

    def flush(self):
        pass
    


class PipeStream(StreamWrap):
    
    def getAttributes(self, pipe):
        read = pipe.stdout.read
        write = pipe.stdin.write
        flush = pipe.stdin.flush
        stream = None
        return locals()


class StdIOStream(StreamWrap):
    
    def getAttributes(self):
        write = sys.stdout.write
        read = sys.stdin.read
        if hasattr(sys.stdin, 'readline'):
            readline = sys.stdin.readline
        else:
            def readline():
                c = ''
                s = ''
                while c != '\n':
                    c = read(1)
                    if c == '':
                        time.sleep(0.001)
                    s+= c
                return s
        stream = sys.stdout
        return locals()
    

def SocketStream(sock):
    f = FileStream.FileStream(sock.makefile('rwb'))
    f.socket = sock
    return f        
        
class SocketStream(StreamWrap):

    def getAttributes(self, stream):
        try:
            rdbufsize = stream.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        except socket.error:
            rdbufsize = 8096
        def read(size = rdbufsize):
            return stream.recv(size)
        write = stream.sendall
##        def write(s):
##            print 'write:', repr(s)
##            r = sock.send(s)
##            print len(s), r
##            return r
        stream = sock = stream
        close = stream.close
##        def close():
##            print 'closed!', stream
##            stream.close()
        return locals()


def forList(func):
    '''binds the first argument of map to this function'''
    def forlist(l, *args, **kw):
        return [func(v, *args, **kw) for v in l]
    return forlist

class WrapReadFactory(Stream):
    '''
WrapReadFactory(stream, function, *args, **kw)

the function will be applied to each value read, args and kw
use forList(function) to handle read lists

'''

    def __init__(self, stream, func, *args, **kw):
        Stream.__init__(self, stream)
        self.func = func
        self.args = args
        self.kw = kw
        self._overtake_attribute('update')
        self._overtake_attribute('close')

    def read(self, *args):
        v = self.stream.read(*args)
        return self.func(v, *self.args, **self.kw)


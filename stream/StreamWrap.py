
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
        stream = sock = stream
        close = stream.close
##        def close():
##            print 'closed!', stream
##            stream.close()
        return locals()


class WrapReadFactory(Stream):

    def __init__(self, stream, func, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw
        Stream.__init__(self, stream)

    def read(self, *args):
        v = self.stream.read(*args)
        return func(v, *self.args, **self.kw)

    def update(self):
        return self.stream.update()

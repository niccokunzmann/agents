
from Stream import *

import sys
import time

import StringStream
import FileStream

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
        return locals()
    

def SocketStream(sock):
    f = FileStream.FileStream(sock.makefile('rwb'))
    f.socket = sock
    return f        
        


from Stream import *

import sys

_l =[]

class DebugStream(Stream):

    def __init__(self, stream, name = '', to = sys.stdout):
        Stream.__init__(self, stream)
        self.name = name
        self.to = to

    def flush(self):
        print >> self.to, 'flush %s:' % self.name,
        r = self.stream.flush()
        print(r)
        return r

    def update(self):
        print >> self.to, 'update %s' % self.name,
        r = self.stream.update()
        print(r)
        return r

    def fileno(self):
        print >> self.to, 'fileno %s' % self.name,
        r = self.stream.fileno()
        print(r)
        return r

    def read(self, arg = _l):
        print >> self.to, 'read %s:' % self.name,
        if arg is not _l:
            print >> self.to, repr(arg)
            obj = self.stream.read(arg)
        else:
            print >> self.to
            obj = self.stream.read()
        print >> self.to, 'read: %s' % self.name, repr(obj)
        return obj
        
    def write(self, arg):
        print >> self.to, 'write %s:' % self.name, repr(arg)
        obj = self.stream.write(arg)
        print >> self.to, 'written: %s' % self.name, repr(obj)
        return obj
    
    def readline(self):
        print >> self.to, 'readline %s:' % self.name
        obj = self.stream.readline()
        print >> self.to, 'readline: %s' % self.name, repr(obj)
        return obj

    def readlines(self, arg = _l):
        print >> self.to, 'readlines %s:' % self.name,
        if arg is not _l:
            print >> self.to, repr(arg)
            obj = self.stream.readlines(arg)
        else:
            print
            obj = self.stream.readlines()
        print >> self.to, 'readlines: %s' % self.name, repr(obj)
        return obj

    def close(self):
        print >> self.to, 'close %s' % self.name
        self.stream.close()

from Stream import *


UNLIMITED_BUFFER = -1
    
class CachingStringStream(Stream):

    def __init__(self, stream, bufsize = UNLIMITED_BUFFER):
        'cache the input and output of this stream. \n'\
        'bufsize is the size of data written before automatically flushing\n'
        Stream.__init__(self, stream)
        self._bufsize = bufsize
        self._read_len = 0
        self._read_buf = []
        self._write_len = 0
        self._write_buf = []

    def write(self, value):
        'cache data'
        self._write_buf.append(value)
        self._write_len+= len(value)
        if self._write_len > self._bufsize > -1:
            return self.flush()

    def flush(self):
        'write all cached data to the next level'
        s = str().join(self._write_buf)
        i = self.stream.write(s)
        if type(i) is int: 
            self._write_buf = [s[i:]]
            self._write_len = len(s) - i
        else:
            self._write_buf = []
            self._write_len = 0
        self.stream.flush()
        return i

    def update(self):
        'update the string\nread data and cache it'
        if self._bufsize == -1:
            s = self.stream.read()
        else:
            l = self._bufsize - self._read_len
            if l <= 0:
                return
            s = self.stream.read(l)
        self._read_len += len(s)
        self._read_buf.append(s)

    def read(self, size = -1):
        'read an amount of characters from the string'
        if size == -1:
            s = str().join(self._read_buf)
            self._read_buf = []
            self._read_len = 0
            return s
        s = str()
        while len(s) < size and self._read_buf:
            s+= self._read_buf.pop(0)
        if len(s) > size > -1:
            self._read_buf.insert(0, s[size:])
            self._read_len -= size
            return s[:size]
        self._read_len -= len(s)
        return s

    def readline(self):
        'read a line from the string or all data'
        i = 0
        c = 0
        i2 = -1
        while i < len(self._read_buf):
            i2 = self._read_buf[i].find('\n')
            if i2 != -1:
                c+= i2
                break
            c+= len(self._read_buf[i])
            i+= 1
        if i2 == -1:
            return self.read()
        return self.read(c + 1)

    def readlines(self, sizehint = 0): # from StringIO
        """Read until EOF using readline() and return a list containing the
        lines thus read.

        If the optional sizehint argument is present, instead of reading up
        to EOF, whole lines totalling approximately sizehint bytes (or more
        to accommodate a final whole line).
        """
        total = 0
        lines = []
        line = self.readline()
        while line[-1:] == '\n': # here the difference
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline()
        return lines # also in FileStream, StringStream

    def writelines(self, lines):
        'write the list of lines to the stream not adding any characters'
        for line in lines:
            self.write(line)

    
import StreamFactory
StreamFactory.registerStream(CachingStringStream, None, \
        lambda stream: (stream.stream, stream._bufsize))
    












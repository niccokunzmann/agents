from Stream import *


UNLIMITED_BUFFER = -1
    
class CachingStringStream(Stream):

    def __init__(self, stream, bufsize = UNLIMITED_BUFFER):
        Stream.__init__(self, stream)
        self._bufsize = bufsize
        self._read_len = 0
        self._read_buf = []
        self._write_len = 0
        self._write_buf = []

    def write(self, value):
        self._write_buf.append(value)
        self._write_len+= len(value)
        if self._write_len > self._bufsize > -1:
            return self.flush()

    def flush(self):
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
    
    












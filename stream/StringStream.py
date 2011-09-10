from Stream import *

class StringStream(Stream):
    def __init__(self, string= str(), index= 0):
        Stream.__init__(self, None)
        self.string= string
        self.index= index

    def read(self, size= None):
        if size is None:
            s= self.string[self.index:]
            self.index= len(s)
            return s
        s= self.string[self.index: self.index + size]
        self.index += len(s)
        return s

    def write(self, s):
        self.string+= s

    def tell(self):
        return self.index

    def seek(self, index):
        self.index= index

    def close(self, *args):
        del self.string

    def flush(self):
        pass

    def readline(self):
##        print '\n##', self.index, type(self.index)
##        print repr(self.string)
        i = self.string.find('\n', self.index)
        if i == -1:
            return self.read()
        return self.read(i - self.index + 1)

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
        return lines

    def update(self):
        pass
            

__all__ = ['StringStream']

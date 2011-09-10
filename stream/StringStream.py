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
        #return len(s)

    def tell(self):
        return self.index

    def seek(self, index):
        self.index= index

    def close(self, *args):
        del self.string

    def flush(self):
        pass

__all__ = ['StringStream']

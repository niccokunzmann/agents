
from Stream import *

import StreamFactory

class EndlessStringStream(Stream):
    def __init__(self, string = ''):
        Stream.__init__(self, None)
        self.string = string

    def read(self, size = None):
        return self.string

    def update(self):
        pass

    def flush(self):
        pass

    def write(self, s):
        self.string+= s


StreamFactory.registerStream(EndlessStringStream, None, \
                             lambda e: e.string)


from Stream import *

import select

class MultiStream(Stream):

    def __init__(self, streams):
        Stream.__init__(self, streams)

    def write(self, obj):
        for stream in self.stream:
            stream.write(obj)

    def flush(self):
        for stream in self.stream:
            stream.flush()

    def read(self, count):
        rd, wt, x = select.select(self.stream, [], [], 0)
        if rd:
            return rd[0].read(count)
        return ''

    def update(self):
        for stream in self.stream:
            stream.update()

    def close(self):
        for stream in self.stream:
            stream.close()

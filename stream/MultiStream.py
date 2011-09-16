
from Stream import *

import select

class MultiStream(Stream):
    '''This stream reads from the first stream that qields a value
the fileno() function is required for every stream passd to this stream

'''

    def __init__(self, streams):
        '''create a MultiStream instance for the streams passed to as list'''
        Stream.__init__(self, streams)

    def write(self, obj):
        '''write the object to each of the streams'''
        for stream in self.stream:
            stream.write(obj)

    def flush(self):
        '''flush all streams'''
        for stream in self.stream:
            stream.flush()

    def read(self, count):
        '''read from the first stream that is ready for reading
and return the value'''
        rd, wt, x = select.select(self.stream, [], [], 0)
        if rd:
            return rd[0].read(count)
        return ''

    def update(self):
        '''update all streams'''
        for stream in self.stream:
            stream.update()

    def close(self):
        '''close all streams'''
        for stream in self.stream:
            stream.close()

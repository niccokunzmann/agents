

from Stream import *

import select
import Queue

class MultiStream(Stream):
    '''This stream reads from the first stream that qields a value
the fileno() function is required for every stream passd to this stream

'''

    def __init__(self, streams):
        '''create a MultiStream instance for the streams passed to as list'''
        Stream.__init__(self, [])
        self._queue = Queue.Queue()
        for stream in streams:
            self.addStream(stream)
        
    def write(self, obj):
        '''write the object to each of the streams'''
        stream = self._queue.get()
        try:
            return stream.write(obj)
        finally:
            self._queue.put(stream)

    def flush(self):
        '''flush all streams'''
        for stream in self.stream:
            stream.flush()

    def read(self, count):
        '''read from the first stream that is ready for reading
and return the value'''
        print 'MultiStream.read:', self.stream
        rd, wt, x = select.select(self.stream[:], [], [], 0)
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

    def addStream(self, stream):
        '''add a stream to the streams'''
        self._queue.put(stream)
        self.stream.append(stream)

    def fileno(self):
        '''get th efileno of this stream'''
        raise NotImplementedError('not implemented')

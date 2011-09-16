
from Stream import *

UPDATE_ALL = -1

class MultiStreamReader(Stream):

    def __init__(self, streams = None):
        '''create a MultistreamReader that reads from streams
use addStream(stream) to add a stream
'''
        if isinstance(streams, Stream):
            Stream.__init__(self, [streams])
        elif streams is None:
            Stream.__init__(self, list())
        else:
            Stream.__init__(self, streams)
        self._streamCount = 1
            

    def read(self, count = -1):
        '''read from the streams until count is achieved
count -1 indicates that all data will be read from the streams'''
        l = []
        if count == -1:
            for stream in self.stream:
                v = stream.read()
                l.extend(v)
            return l
        streamCount = 0
        for stream in self.stream:
            v = stream.read(count - len(l))
            if type(v) is not list:
                raise ValueError('the value read from %r must be of type list'\
                                 % stream)
            streamCount+= 1
            l.extend(v)
            if len(l) >= count:
                break
        self._streamCount = streamCount
        return l

    def update(self, count = None):
        '''update the streams
if count is None the streams that was read form will be updated
if count == UPDATE_ALL all streams will be updated
else the number count of streams will be updated
'''
        if count is None:
            count = self._streamCount
        count -= 1
        for i, stream in enumerate(self.stream[:]):
            if i > count > -2:
                break
            stream.update()

    def addStream(self, stream):
        '''add a stream to read from
the stream is only added if i is not already added'''
        if stream not in self.stream:
            self.stream.append(stream)

from Stream import Stream

import pickle
import StreamFactory

class NoValue(object):
    ''' Singleton Object noValue

'''
    def __reduce__(self):
        return 'noValue'

    def __call__(self, *args, **kw):
        '''this call does nothing'''
        return self

noValue = NoValue()

del NoValue

class PickleStream(Stream):

    def __init__(self, stream):
        Stream.__init__(self, stream)
        self._setPickler()
        self._setUnpickler()
        self._overtake_attribute('fileno')
        self._overtake_attribute('flush')

        self._buffer = []
    
    def _setPickler(self):
        self._pickler = pickle.Pickler(self.stream)
    
    def _setUnpickler(self):
        self._unpickler = pickle.Unpickler(self.stream)

    def read(self, size = -1):
        'size is ignored'
        if size == -1:
            r = self._buffer[:]
            self._buffer = []
        else:
            r = self._buffer[:size]
            self._buffer = self._buffer[size:]
        return r

    def update(self):
        self.stream.update()
        o = self._unpickler.load()
        if o is not noValue:
            self._buffer.append(o)

    def write(self, obj):
        return self._pickler.dump(obj)

StreamFactory.registerStream(PickleStream, None, StreamFactory.streamArguments)




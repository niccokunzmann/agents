from Stream import Stream

class NoValue(object):
    ''' Singleton Object noValue

'''
    def __reduce__(self):
        return 'noValue'

    def __call__(*args):
        '''this call does nothing'''
        pass

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
        self._pickler = pickle.Pickler(self._stream)
    
    def _setUnpickler(self):
        self._unpickler = pickle.Unpickler(self._stream)

    def read(self, size = None):
        'size is ignored'
        if not self.buffer:
            self.update()
        r = self.buffer[:]
        self.buffer = []
        return r

    def update(self):
        self.stream.update()
        o = self._unpickler.load()
        if o is not noValue:
            self.buffer.append(o)

    def write(self, obj):
        return self._pickler.dump(obj)

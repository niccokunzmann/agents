from Stream import Stream

import pickle

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
        self._pickler = pickle.Pickler(self.stream)
    
    def _setUnpickler(self):
        self._unpickler = pickle.Unpickler(self.stream)

    def read(self, size = None):
        'size is ignored'
        if not self._buffer:
            self.update()
        r = self._buffer[:]
        self._buffer = []
        return r

    def update(self):
        self.stream.update()
        o = self._unpickler.load()
        if o is not noValue:
            self._buffer.append(o)

    def write(self, obj):
        return self._pickler.dump(obj)

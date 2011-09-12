import thread

from StringStream import *

thread_error= thread.error

class BlockingStringStream(StringStream):

    def __init__(self, *args, **kw):
        StringStream.__init__(self, *args, **kw)
        self._lock= thread.allocate_lock()
        self._noData_lock= thread.allocate_lock()
        self.__closed = False

    def read(self, *args, **kw):
        while 1:
            with self._lock:
                data= StringStream.read(self, *args, **kw)
                if data or self.__closed:
                    return data
                self._noData_lock.acquire(False)
            self._noData_lock.acquire()
            try:
                self._noData_lock.release()
            except thread_error:
                pass

    def write(self, *args, **kw):
        if self.__closed:
            raise IOError('stream closed')
        with self._lock:
            r= StringStream.write(self, *args, **kw)
            try:
                self._noData_lock.release()
            except thread_error:
                pass
        return r

    def close(self):
        self.__closed = True

import StreamFactory

StreamFactory.registerStream(BlockingStringStream, None, \
                             lambda s: (s.string, s.index))

__all__= ['BlockingStringStream']

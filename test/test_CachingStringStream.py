
from test import *

from stream.CachingStringStream import CachingStringStream, UNLIMITED_BUFFER
from stream.StringStream import StringStream


class test_CachingStringStream(unittest.TestCase):

    bufsize = UNLIMITED_BUFFER

    def newStream(self, s = ''):
        return CachingStringStream(StringStream(s), self.bufsize)

    def test_bufsize(self):
        self.newStream()._bufsize == -1

    def test_bufsize_eq(self):
        self.newStream()._bufsize == self.bufsize
    
    def test_read(self):
        s = self.newStream()
        self.assertEquals('', s.read())
        self.assertEquals('', s.read())

    def test_read_update(self):
        s = self.newStream('lalilu')
        self.assertEquals('', s.read())
        s.update()
        self.assertEquals('lali', s.read(4))
        if self.bufsize < 6:
            s.update()
        self.assertEquals('lu', s.read())

    def test_write(self):
        s = self.newStream()
        s.write('lalilu')
        self.assertEquals('', s.read())
        s.update()
        self.assertEquals('', s.read())
        s.flush()
        self.assertEquals('', s.read())
        s.update()
        self.assertEquals('la', s.read(2))
        s.write('hello!')
        s.update()
        s.flush()
        self.assertEquals('lilu', s.read())
        s.update()
        self.assertEquals('hell', s.read(4))
        self.assertEquals('o!', s.read())
        s.update()
        self.assertEquals('', s.read())
    

class test_CachingStringStream_bigBuffer(test_CachingStringStream):

    bufsize = 30
    
    def test_bufsize(self):
        self.newStream()._bufsize == 30
    
class test_CachingStringStream_tinyBuffer(test_CachingStringStream):

    bufsize = 1
    
    def test_bufsize(self):
        self.newStream()._bufsize == 1

    test_write = unittest.expectedFailure(\
        test_CachingStringStream.test_write)
    test_read_update = unittest.expectedFailure(\
        test_CachingStringStream.test_read_update)
    
class test_CachingStringStream_smallerBuffer(test_CachingStringStream):

    bufsize = 4
    
    def test_bufsize(self):
        self.newStream()._bufsize == 4
    
    test_write = unittest.expectedFailure(\
        test_CachingStringStream.test_write)
    
class test_CachingStringStream_smallBuffer(test_CachingStringStream):

    bufsize = 6
    
    def test_bufsize(self):
        self.newStream()._bufsize == 6

    




def test_module():
    unittest.main(exit = False, verbosity = 1)

if __name__ == '__main__':
    test_module()


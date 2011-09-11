
from test import *

from stream.CachingStringStream import CachingStringStream
from stream.StringStream import StringStream


class test_CachingStringStream(unittest.TestCase):

    def newStream(self, s = ''):
        return CachingStringStream(StringStream(s))

    def test_read(self):
        s = self.newStream()
        self.assertEquals('', s.read())
        self.assertEquals('', s.read())

    def test_read_update(self):
        s = self.newStream('lalilu')
        self.assertEquals('', s.read())
        s.update()
        self.assertEquals('lali', s.read(4))
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
    




def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()


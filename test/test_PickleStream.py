
from test import *

from stream.PickleStream import PickleStream, noValue
from stream.FileStream import FileStream
from stream.StringStream import StringStream


class test_PickleStream(unittest.TestCase):

    def setup(self):
        pass

    l = ['hallo', 1, 1L, [], noValue, ArithmeticError]

    def test_create(self):
        s = StringStream()
        p = PickleStream(s)
        
    def test_write(self):
        s = StringStream()
        p = PickleStream(s)
        for e in self.l:
            p.write(e)
        return s


    def test_read(self):
        s = self.test_write()
        p = PickleStream(s)
        l = []
        for i in range(len(self.l)):
            l.extend(p.read())
        assertEquals(self.l, l)


def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()

    

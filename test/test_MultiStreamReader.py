
from test import *

from stream.MultiStreamReader import MultiStreamReader

from stream.Stream import Stream

L = 'a b c d'.split()

class MockStream(Stream):

    def __init__(self):
        Stream.__init__(self, None)
        self.l = L
        self.updates= 0
        self.closes = 0
        self.reads = 0

    def read(self, count = 50):
        self.reads+= 1
        r = self.l[:count]
        self.l = self.l[count:]
        return r

    def update(self):
        self.updates+= 1

    def close(self):
        self.closes+= 1

class test_MultiStreamReader(unittest.TestCase):

    def setUp(self):
        self.m0 = MultiStreamReader()
        
    def m(self, c):
        return MultiStreamReader([MockStream() for i in range(c)])

    def test_read0(self):
        self.assertEqual([], self.m(0).read())

    def test_read00(self):
        self.assertEqual([], self.m(0).read(0))

    def test_read01(self):
        self.assertEqual([], self.m(0).read(1))

    def test_1(self):
        m = self.m(1)
        self.assertEqual([], m.read(0))
        self.assertEqual(['a'], m.read(1))
        self.assertEqual([], m.read(0))
        self.assertEqual(['b', 'c'], m.read(2))
        self.assertEqual([], m.read(0))
        self.assertEqual(['d'], m.read(3))
        self.assertEqual([], m.read(0))
        self.assertEqual([], m.read(4))
        self.assertEqual([], m.read(0))
        self.assertEqual([], m.read(5))
        
    def test_2(self):
        m = self.m(2)
        self.assertEqual([], m.read(0))
        self.assertEqual(['a'], m.read(1))
        self.assertEqual([], m.read(0))
        self.assertEqual(['b', 'c'], m.read(2))
        self.assertEqual([], m.read(0))
        self.assertEqual(['d', 'a', 'b'], m.read(3))
        self.assertEqual([], m.read(0))
        self.assertEqual(['c', 'd'], m.read(4))
        self.assertEqual([], m.read(0))
        self.assertEqual([], m.read(5))
        
    def test_30(self):
        m = self.m(3)
        self.assertEqual([], m.read(0))
        self.assertEqual(['a'], m.read(1))
        self.assertEqual([], m.read(0))
        self.assertEqual(['b', 'c'], m.read(2))
        self.assertEqual([], m.read(0))
        self.assertEqual(['d', 'a', 'b'], m.read(3))
        self.assertEqual([], m.read(0))
        self.assertEqual(['c'], m.read(1))
        self.assertEqual([], m.read(0))
        self.assertEqual(['d', 'a', 'b', 'c'], m.read(4))
        self.assertEqual([], m.read(0))
        self.assertEqual(['d'], m.read(5))
        self.assertEqual([], m.read(0))
        self.assertEqual([], m.read())
        
    def test_3(self):
        m = self.m(3)
        self.assertEqual(['a'], m.read(1))
        self.assertEqual(['b', 'c'], m.read(2))
        self.assertEqual(['d', 'a', 'b'], m.read(3))
        self.assertEqual(['c'], m.read(1))
        self.assertEqual(['d', 'a', 'b', 'c'], m.read(4))
        self.assertEqual(['d'], m.read(5))
        self.assertEqual([], m.read())

    def test_1_all(self):
        self.assertEqual(L*1, self.m(1).read())
        
    def test_2_all(self):
        self.assertEqual(L*2, self.m(2).read())

    def test_6_all(self):
        self.assertEqual(L*6, self.m(6).read())

    def test_600_all(self):
        self.assertEqual(L*600, self.m(600).read())

    def test_600_100(self):
        self.maxDiff = None
        self.assertEqual((L*600)[:100], self.m(600).read(100))


    def test_read_update(self):
        m = self.m(2)
        self.assertEqual(['a'], m.read(1))
        self.assertEqual(1, m._streamCount)
        m.update()
        self.assertEqual(1, m.stream[0].updates)
        self.assertEqual(0, m.stream[1].updates)
        return m

    def test_read_update_read_update(self):
        m = self.test_read_update()
        self.assertEqual(0, m.stream[1].reads)
        self.assertEqual(1, m.stream[0].reads)
        m.read(len(L) - 1)
        self.assertEqual(0, m.stream[1].reads)
        m.update()
        self.assertEqual(2, m.stream[0].updates)
        self.assertEqual(0, m.stream[1].updates)

    def test_streamCount(self):
        self.assertTrue(-1, self.m(0)._streamCount)

    def test_create_update(self):
        m = self.m(3)
        for i in range(8):
            for j, s in enumerate(m.stream):
                self.assertEqual((i if not j else 0), s.updates, '%i %i' % (i, j))
            m.update()
        
    
if __name__ == '__main__':
     unittest.main(exit = False, verbosity = 2)       

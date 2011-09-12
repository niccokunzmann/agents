from test import *


import stream.StringStream


from stream.StringStream import StringStream

class test_StringStream(unittest.TestCase):

    def newStream(self, *args):
        return StringStream(*args)

    def test_create(self):
        return self.newStream()

    def test_create_args(self):
        return self.newStream('args')

    def test_read_args(self):
        s = self.test_create_args()
        a = s.read(4)
        self.assertEquals('args', a)
        self._test_empty(s)

    def test_read_args_all(self):
        s = self.test_create_args()
        a = s.read()
        self.assertEquals('args', a)
        self._test_empty(s)

    def test_write(self):
        s = self.newStream('args')
        s.write('lalilu')
        s.flush()
        return s

    def test_write_read(self):
        s = self.test_write()
        self.assertEqual('args', s.read(4))
        self.assertEqual('lalilu', s.read(6))
        self._test_empty(s)
        
    def test_write_read_all(self):
        s = self.test_write()
        self.assertEqual('argslalilu', s.read(10))
        self._test_empty(s)

    def _test_empty(self, s):
        self.assertEqual('', s.read(6))

    def test_complex_1(self):
        self._test_empty(self.s1())

    def s1(self):
        s = self.newStream()
        s.write('lalilu')
        self.assertEquals('la', s.read(2))
        s.update()
        s.write('hell')
        s.flush()
        s.update()
        self.assertEquals('liluhell', s.read())
        s.flush()
        return s

    def test_complex_2(self):
        s = self.s1()
        s.update()
        s.write('lalilu')
        self.assertEquals('la', s.read(2))
        s.write('hello!')
        s.update()
        s.flush()
        self.assertEquals('lilu', s.read(4))
        s.update()
        self.assertEquals('hell', s.read(4))
        self.assertEquals('o!', s.read())
        s.update()
        self._test_empty(s)

    def test_ser(self):
        self.ser_eq(self.newStream())

    def test_ser_spe(self):
        s = self.newStream()
        s.write('lailul354562738344')
        s.read(5)
        self.ser_eq(s)

    def ser_eq(self, s1):
        s2 = test_factory(self, s1)
        self.assertEqual(s1.index, s2.index)
        self.assertEqual(s1.string, s2.string)
        


def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()

    

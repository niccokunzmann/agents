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
        


def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()

    

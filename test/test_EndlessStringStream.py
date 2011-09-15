
from test import *

from stream.EndlessStringStream import EndlessStringStream

class test_EndlessStringStream(unittest.TestCase):

    def test_create(self):
        return EndlessStringStream()
        
    def test_create_arg(self):
        return EndlessStringStream('lalilu')

    def test_read(self):
        s = self.test_create_arg()
        self.assertEqual('lalilu', s.read())

    def test_read_arg(self):
        s = self.test_create_arg()
        self.assertEqual('lalilu', s.read(234))

    def test_read_arg2(self):
        s = self.test_create_arg()
        self.assertEqual('lalilu', s.read(0))

    def test_write(self):
        s = self.test_create_arg()
        s.write('!')
        self.assertEqual('lalilu!', s.read())



if __name__ == '__main__':
    unittest.main(exit = None)

from test import *

from stream.BrokenStream import BrokenStream
from stream.BrokenStream import BrokenStreamError
from stream.BrokenStream import StreamClosedError

class test_BrokenStream(unittest.TestCase):

    def newObject(self):
        return BrokenStream()

    error = BrokenStreamError

    def test_read(self):
        self.assertRaises(self.error, self.newObject().read)

    def test_read_arg(self):
        self.assertRaises(self.error, self.newObject().read, 1)

    def test_flush(self):
        self.assertRaises(self.error, self.newObject().flush)

    def test_write(self):
        self.assertRaises(self.error, self.newObject().write, 1)

    def test_update(self):
        self.assertRaises(self.error, self.newObject().update)


class test_BrokenStream_closed(test_BrokenStream):

    def newObject(self):
        b = BrokenStream()
        b.close()
        return b

    error = StreamClosedError

def test_module():
    unittest.main(exit = False, verbosity = 1)

if __name__ == '__main__':
    test_module()

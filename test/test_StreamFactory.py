

from test import *

from stream.StringStream import StringStream


from stream.StreamFactory import *

import stream.BrokenStream as BrokenStream


class MyStream(BrokenStream.BrokenStream):
    pass

class test_StreamFactory(unittest.TestCase):

    def setUp(self):
        self.fac = self.newFac()

    def newFac(self):
        return StreamFactory(StringStream())

    def test_create(self):
        fac = self.newFac()
    
    def test_register_random_string(self):
        fac = self.newFac()
        self.assertRaises(ValueError, fac.registerStream, 'kghasdfjhjdagf')
        
    def test_register_BrokenStream_str(self):
        fac = self.newFac()
        reg = streamRegister
        self.assertIn(BrokenStream.BrokenStream, reg)
        fac.registerStream('BrokenStream')

    def test_register_BrokenStream_cls(self):
        fac = self.newFac()
        fac.registerStream(BrokenStream.BrokenStream)

    def test_write_BrokenStream_err(self):
        self.assertRaises(StreamNotRegistered, self.fac.write, BrokenStream.BrokenStream())

    def test_write_BrokenStream(self):
        self.fac.registerStream(BrokenStream.BrokenStream)
        self.fac.write(BrokenStream.BrokenStream())
        self.fac.flush()

    def test_read_write_BrokenStream(self):
        self.test_write_BrokenStream()
        self.fac.update()
        bs = self.fac.read(1)
        self.assertIsInstance(bs, BrokenStream.BrokenStream)

    def test_stream_cascade(self):
        self.fac.registerStream(BrokenStream.BrokenStream)
        self.fac.registerStream(StringStream)
        import stream.CachingStringStream as CachingStringStream
        self.fac.registerStream(CachingStringStream.CachingStringStream)
        s = StringStream()
        s = BrokenStream.BrokenStream(s)
        s = CachingStringStream.CachingStringStream(s)
        self.fac.write(s)
        self.fac.flush()
        self.fac.update()
        s2 = self.fac.read()
        self.assertIsInstance(s, CachingStringStream.CachingStringStream)
        self.assertIsInstance(s, BrokenStream.BrokenStream)
        self.assertIsInstance(s, StringStream)

    def test_do_readWrite(self):
        bs = BrokenStream.BrokenStream()
        bs2 = do_readWrite(bs)
        self.assertIsInstance(bs2, BrokenStream.BrokenStream)

    def test_import(self):
        l = []
        from stream.StreamFactory import StreamFactory as a
        c = b = a
        try:
            from StreamFactory import StreamFactory as c
            l.append(StreamFactory)
        except ImportError:
            pass
        try:
            from distobj.stream.StreamFactory import StreamFactory as b
        except ImportError:
            pass
        self.assertIs(a, b)
        self.assertIs(a, c)

    def test_register_MyStream(self):
        registerStream(MyStream)
        reg = streamRegister
        self.assertIn(MyStream, reg)
        self.assertIn(MyStream.__name__, reg)
        self.assertIn(MyStream.__module__ + '.' + MyStream.__name__, reg)


def test_module():
    unittest.main(exit = False, verbosity = 1)

if __name__ == '__main__':
    test_module()

from test import *

from log import logClass, StreamLog

from stream.StringStream import StringStream

class test_logClass(unittest.TestCase):


    def test_log_getId(self):
        i = StreamLog.getId()
        i2 = StreamLog.getId()
        self.assertNotEqual(i, i2, 'different ids')
        self.assertEqual(i, StreamLog.getId(i))

    def test_log_class(self):

        s = StringStream()
        log = StreamLog(s)

        @logClass(log, 'method'.split())
        class MyCls(object):
            def method(self, args):
                return args
            
        l = len(s.string)
        _id = int(StreamLog.getId())
        self.assertNotEqual(0, l, 'something written')
        self.assertIn(MyCls.__name__, s.string)
        o = MyCls()
        self.assertEqual(l, len(s.string), '__init__ not monitored')
        o.method('lalilu')
        self.assertNotEqual(0, l, 'something written')
        self.assertIn('lalilu', s.string[l:])
        self.assertIn('method', s.string[l:])
        l = len(s.string)
        self.assertEqual(_id + 2, int(StreamLog.getId()))
        print s.string


if __name__ == '__main__':
    unittest.main(exit = False)
        

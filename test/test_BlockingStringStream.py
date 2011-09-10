from test import *


import stream.StringStream


from stream.BlockingStringStream import BlockingStringStream

from test_StringStream import *

import thread
import time

class test_BlockingStringStream(test_StringStream):

    def newStream(self, *args):
        return BlockingStringStream(*args)

    def wait_call(self, sec, func, *args, **kw):
        def call():
            time.sleep(sec)
            func(*args, **kw)
        thread.start_new(call, ())
    
    def test_async_readWrite(self):
        s = self.newStream()
        self.wait_call(0.01, s.write, 'hello!')
        hello = s.read(6)
        self.assertEquals('hello!', hello)
        self._test_empty(s)
        
    def _test_empty(self, s):
        s.close()
        self.assertEqual('', s.read(6))

    def test_closed(self):
        s = self.newStream()
        self._test_empty(s)
        


def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()

    

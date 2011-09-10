
from test import *

from stream.PickleStream import PickleStream, noValue

class test_PickleStream(unittest.TestCase):

    def setup(self):
        pass

    def test_create(self):
        s = io.BytesIO()
        p = PickleStream(s)
        
    def test_write(self):
        s = io.BytesIO()
        p = PickleStream(s)
        p.write('hallo')        
        p.write(1)        
        p.write(1L)        
        p.write([])        
        p.write(noValue)
        p.write(ArithmeticError)
        return s


    def test_read(self):
        s = test_write()
        s.seek(0)
        p = PickleStream(s)
        

def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()

    

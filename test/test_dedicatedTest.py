#!/bin/env python
from test import *

objectList = [1,\
              12434, \
              63577642572436562835, \
              [], \
              u"15637", \
              'lalilu', \
              ]

objectList.append(objectList)

debug = 0

class test_dedicatedTest(unittest.TestCase):

    
    def dedicated_equals(self, obj):
        if debug:print 0
        s = launchDedicatedTest('test_echo_dedicated.py')
        if debug:print 1
        s.write(obj)
        s.flush()
        if debug:print 2
        try:
            if debug:print 3
            b = s.printOnFail()
            if debug:print 4
            self.assertTrue(b)
        except:
            ty, er, tb = sys.exc_info()
            raise ty, er, tb
        if debug:print 5
        s.update()
        o2 = s.read()[0]
        if debug:print 6
        try:
            self.assertEqual(obj, o2, 'objects equal')
        except RuntimeError:
            self.assertTrue(True)
        if debug:print 7
        return o2

    def test_0(self):
        self.dedicated_equals(objectList[0])
    def test_1(self):
        self.dedicated_equals(objectList[1])
    def test_2(self):
        self.dedicated_equals(objectList[2])
    def test_3(self):
        self.dedicated_equals(objectList[3])
    def test_4(self):
        self.dedicated_equals(objectList[4])
    def test_5(self):
        self.dedicated_equals(objectList[5])
    def test_6(self):
        self.dedicated_equals(objectList[6])

def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()


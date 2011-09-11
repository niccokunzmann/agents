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
        l = []
        o2 = dedicated_echo(obj, l, test = 'test_echo_dedicated.test_echo_inlist')
        self.assertFalse(o2 is l, 'the echo of the object %s failed' % obj)
        try:
            self.assertEqual(obj, o2, 'objects equal')
        except RuntimeError:
            self.assertTrue(True)
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

    def test_start_TestCaseClass(self):
        s = launchDedicatedTest('test_echo_dedicated.py', \
                                'test_echo_dedicated.test_echo')
        s.write(1)
        s.flush()
        self.assertTrue(s.printOnFail())
        s.update()
        o = s.read()[0]
        self.assertEqual(1, o, 'objects equal')
        
    def test_start_TestCaseMethod(self):
        s = launchDedicatedTest('test_echo_dedicated.py', \
                                'test_echo_dedicated.test_echo')
        s.write(1)
        s.flush()
        self.assertTrue(s.printOnFail())
        s.update()
        o = s.read()[0]
        self.assertEqual(1, o, 'objects equal')

def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()


#!/bin/env python
from test import *

from objects.GlobalObject import GlobalObject
from TestGlobalObject import TestGlobalObject

import test_GlobalObject

class test_GlobalObject(unittest.TestCase):

    def test_create(self):
        o = GlobalObject('test_create')

    def test_create_subclass(self):
        l = []
        o = TestGlobalObject('test_create_subclass', l)
        l2 = o.args[0]
        self.assertTrue(l2 is l)

    def test_unique(self):
        o = TestGlobalObject('test_unique')
        o2 = TestGlobalObject('test_unique')
        
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)

    def test_pickle_subclass(self):
        o = TestGlobalObject('test_pickle_subclass')
        o2 = pickle_unpickle(o)
        
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)
    
    def test_pickle(self):
        o = GlobalObject('test_pickle')
        o2 = pickle_unpickle(o)
        
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)

    def test_dedicated(self):
        s = launchDedicatedTest('test_GlobalObject_dedicated.py')
        o = TestGlobalObject('test_dedicated')
        s.write(o)
        s.flush()
        self.assertTrue(s.printOnFail())
        try:
            self.assertEqual(o.__class__, s.read()[0]) #1
            self.assertEqual(o.__reduce__()[0], s.read()[0]) #2
            self.assertEqual(o.__reduce__()[1], s.read()[0]) #3
            o2 = s.read()[0] #4
        except :
            ty, er, tb = sys.exc_info()
            raise ty, er, tb
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)
        


def replace_import():
    try:    __imp_old = __builtins__['__import__']
    except: __imp_old = __builtins__.__import__
    def __import__(*args, **kw):
        print '__import__', args, kw,
        try:
            r= __imp_old(*args, **kw)
        except:
            print 'fail'
            raise
        else:
            print 'ok'
        return r
        

    try:    __builtins__['__import__'] = __import__
    except: __builtins__.__import__ = __import__
    
def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()

    

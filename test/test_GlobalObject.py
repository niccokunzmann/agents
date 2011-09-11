#!/bin/env python
from test import *

from objects.GlobalObject import GlobalObject
from TestGlobalObject import TestGlobalObject

import test_GlobalObject

class test_GlobalObject(unittest.TestCase):

    def newObject(self, name, *args):
        return GlobalObject(name, *args)

    def test_create(self):
        o = self.newObject('test_create')

    def test_unique(self):
        o = self.newObject('test_unique')
        o2 = self.newObject('test_unique')
        
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)
    
    def test_pickle(self):
        o = self.newObject('test_pickle')
        o2 = pickle_unpickle(o)
        
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)

    def test_dedicated(self):
        s = launchDedicatedTest('test_GlobalObject_dedicated.py', \
                        'test_GlobalObject_dedicated.test_unique')
        self._test_dedicated(s)
        
    def _test_dedicated(self, s):
        o = self.newObject('test_dedicated')
        s.write(o)
        s.flush()
        self.assertTrue(s.printOnFail())
        try:
            s.update()
            self.assertEqual(o.__class__, s.read()[0]) #1
            s.update()
            self.assertEqual(o.__reduce__()[0], s.read()[0]) #2
            s.update()
            self.assertEqual(o.__reduce__()[1], s.read()[0]) #3
            s.update()
            o2 = s.read()[0] #4
        except :
            ty, er, tb = sys.exc_info()
            raise ty, er, tb
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)

    def test_setDefaultAttribute(self):
        o = self.newObject('test_setDefaultAttribute')
        o.default.x = 2
        self.assertEqual(2, o.x)
        o.default.x = 5
        self.assertEqual(2, o.x)
        o.x = 88
        self.assertEqual(88, o.x)

        o.randomAttribute = 88
        self.assertEqual(88, o.randomAttribute)

    def test_setDefaultAttribute_after(self):
        o = self.newObject('test_setDefaultAttribute_after')
        o.x = 5
        o.default.x = 2
        self.assertEqual(5, o.x)

    def test_setDefaultAttribute_set(self):
        o = self.newObject('test_setDefaultAttribute_set')
        self.assertFalse(o.default.nana)
        o.default.nana = 2
        self.assertTrue(o.default.nana)
        self.assertEqual(2, o.nana)

    def test_name(self):
        o = self.newObject('test_name')
        self.assertEqual('test_name', o.getName())

class test_GlobalObject_subclass(test_GlobalObject):
    
    def newObject(self, name, *args):
        return TestGlobalObject(name, *args)

    def test_create_arg(self):
        l = []
        o = self.newObject('test_create', l)
        self.assertEqual(o.args, (l,))
        self.assertTrue(o.args[0] is l)

    def test_dedicated(self):
        s = launchDedicatedTest('test_GlobalObject_dedicated.py', \
                    'test_GlobalObject_dedicated_subclass.test_unique')
        self._test_dedicated(s)
        



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
    unittest.main(exit = False, verbosity = 1)

if __name__ == '__main__':
    test_module()

    

#!/bin/env python
from test import *

from objects.GlobalObject import GlobalObject

class TestGlobalObject(GlobalObject):

    def __init__(self, name, *args):
        self.args = args

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




if __name__ == '__main__':
    unittest.main(exit = False)

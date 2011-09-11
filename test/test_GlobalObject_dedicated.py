from test import *

from test_GlobalObject import TestGlobalObject

class test_GlobalObject_dedicated(unittest.TestCase):

    def test_unique(self):
        o2 = TestGlobalObject('test_dedicated')
        ps.write(o2.__class__)
        ps.write(o2.__reduce__()[0])
        ps.write(o2.__reduce__()[1])
        ps.write(o2)
        self.assertEqual(o, o2)
        self.assertTrue(o is o2)
        print
        print o2.__class__.__module__
        print o.__class__.__module__
        print o.__reduce__()[0].__module__
        print o.__reduce__()
        print 'lala'

    @unittest.skip('skipping this')
    def test_fail(self):
        self.fail()


if __name__ == '__main__':
##    suite = unittest.TestSuite(())
    ps = beDedicatedTest()
    ps.update()
    o = ps.read()
    while not o:
        ps.update()
        o = ps.read()
    o = o[0]
    unittest.main(exit = False)

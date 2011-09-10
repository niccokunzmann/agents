from test import *

from test_dedicatedTest import objectList


class test_echo_dedicated(unittest.TestCase):

    def test_echo(self):
        ps.update()
        obj = ps.read()[0]
        print 'obj:', obj
        ps.write(obj)
        ps.flush()
        try:
            self.assertIn(obj, objectList, 'unexpected object received')
        except RuntimeError:
            self.assertTrue(True)

    @unittest.skip('skipping this')
    def test_fail(self):
        self.fail()



if __name__ == '__main__':
    ps = beDedicatedTest()
    import thread
    import time
    l = []
    def test():
        try:
            unittest.main(exit = False)
        finally:
            l.append(1)
    thread.start_new(test, ())
    #test()
    doTimeout(lambda :1/len(l), ZeroDivisionError)
    

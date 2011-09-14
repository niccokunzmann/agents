

from test import *

from stream.IPPort import IPPort

class test_built_cluster_dedicated(unittest.TestCase):

    def test_send_manager(self):
        ps.write(True)
        port = IPPort()
        port.broadcast()





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
    doTimeout(lambda :1/len(l), ZeroDivisionError, timeout = 10)

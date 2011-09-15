

from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw
from stream.IPPort import IPPort

debug = True

class test_build_cluster(unittest.TestCase):

    @unittest.skip('todo')
    def test_dedicated_launch(self):
        port = IPPort(('localhost',), (6328,6326))
        ps = launchDedicatedTest('test_build_cluster_dedicated.py', \
                    'test_build_cluster_dedicated.test_send_manager')
        try:
            if debug: print 1
            ps.update()
            if debug: print 2
            started = ps.read()
            if debug: print 3
            self.assertTrue(started)
            if debug: print 4
            port.broadcast()
            if debug: print 5
            l = []
            def do():
                port.update()
                l.extend(port.read(1))
                1/len(l)
            doTimeout(do, ZeroDivisionError)
            self.assertNotEqual([], l, 'nothing received')
            if debug: print 8
            m.connect()
            if debug: print 9
            m.write('hallo!')
            if debug: print 10
            m.flush()
            if debug: print 11
            m.update()
            if debug: print 12
            message = m.read(1)
            if debug: print 13
            self.assertEqual(['hello!'], message)
        finally:
            ps.printOnFail()

        
    @unittest.skip('todo')
    def test_port_broadcast(self):
        p = IPPort()
        p.broadcast()
        p.update()
        l = p.read(1)
        self.assertNotEqual([], l)
        p.close()
        return l[0]

    def test_open_connection(self):
        c = self.test_port_broadcast()
        c.connect()

    def test_broadcast(self):
        pass

    def test_open_close_open(self):
        self.test_close()
        self.test_close()
        
    def test_close(self):
        p = IPPort()
        p.close()



if __name__ == '__main__':
    unittest.main(exit = False)

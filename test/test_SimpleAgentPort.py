
from test import *

from stream.SimpleAgentPort import *

import socket
import thread


class test_SimpleAgentPort(unittest.TestCase):

    def setUp(self):
        self.pl = []
        self.a = a = SimpleAgent('test_SimpleAgentPort')
        self.p = self.newPort(a)
        self.p.open()
        self.con = None

    def tearDown(self):
        for port in self.pl:
            port.close()

    def newPort(self, agent):
        return SimpleAgentPort(agent)

    def test_broadcast(self):
        self.p.broadcast()

    def test_broadcast_recv(self):
        self.p.broadcast()
        time.sleep(0.01)
        self.p.update()
        con = self.p.read(1)
        self.assertNotEqual([], con)
        self.con = con = con[0]
        
    def test_broadcast_recv_connect(self):
        self.test_broadcast_recv()
        c1 = self.con
        c1.connect()
        self.assertTrue(c1.isConnected())

    def test_broadcast_recv_connect_accept(self):
        self.test_broadcast_recv_connect()
        c1 = self.con
        self.p.update()
        c2 = self.p.read(1)
        self.assertNotEqual([], c2)
        return c1, c2[0]

    def test_broadcast_recv_connect_accept_connect(self):
        c1, c2 = self.test_broadcast_recv_connect_accept()
        c2.connect()
        return c1, c2

    def test_write(self):
        c1, c2 = self.test_broadcast_recv_connect_accept_connect()
        c1.write('lalilu')
        c1.flush()
        l = []
        def do():
            c2.update()
            l.extend(c2.read(1))
            1/len(l)
        doTimeout(do, ZeroDivisionError)
        self.assertNotEqual([], l, 'empfang nicht geklappt')
        self.assertEqual(['lalilu'], l)
        a = self.a
        a2 = SimpleAgent('test_write')
        c2.write(self.a)
        c2.write(a2)
        c2.flush()
        l = []
        def par():
            for i in range(4):
                time.sleep(0.01)
                c1.update()
            l.append(1)
        thread.start_new(par, ())
        doTimeout(lambda :1/len(l), ZeroDivisionError)
        self.assertNotEqual([], l, 'update blocked')
        l = c1.read()
        self.assertEqual(2, len(l))
        a_, a2_ = l
        self.assertIs(a, a_, 'sending agent failed')
        self.assertIs(a2, a2_)
        

    def test_addr(self):
        host, port = self.p.getConnectAddress()
        self.assertNotEqual('', host)
        self.assertNotEqual(0, port)
        self.assertNotEqual(None, port)


if __name__ == '__main__':
    unittest.main(exit = False)

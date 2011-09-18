
from test import *

from stream.SimpleAgentPort import *



class test_SimpleAgentPort(unittest.TestCase):

    def setUp(self):
        self.pl = []
        a = SimpleAgent('test_SimpleAgentPort')
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
        pass
        


if __name__ == '__main__':
    unittest.main(exit = False)

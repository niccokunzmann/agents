


from test import *

from stream.SocketAcceptStream import SocketAcceptStream

class test_SocketAcceptStream(unittest.TestCase):

    def setUp(self):
        s = socket.socket()
        s.bind(('localhost', 0))
        s.listen(100)
        s2 = socket.socket()
        s2.bind(('localhost', 0))
        s2.listen(100)
        self.port = s.getsockname()[1]
        self.ports = (self.port, s2.getsockname()[1])
        self.addr = ('localhost', self.port)
        self.addr2 = ('localhost', self.ports[1])
        self.a = SocketAcceptStream([s, s2])

    def test_conn(self):
        s = socket.socket()
        s.connect(self.addr)
        time.sleep(0.01)
        self.a.update()
        l = self.a.read()
        self.assertNotEqual([], l)

    def test_conn2(self, count = 4):
        sock = []
        for i in range(count):
            s = socket.socket()
            s.connect(self.addr)
            sock.append(s)
            self.a.update()
        l = self.a.read(count)
        self.assertNotEqual([], l)
        self.assertEqual(count, len(l))


    def tearDown(self):
        self.a.close()
        

if __name__ == '__main__':
    unittest.main(exit = False)

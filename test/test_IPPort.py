from test import *


from stream.IPPort import *
from stream.StreamWrap import SocketStream
from stream.CachingStringStream import CachingStringStream
from stream.TCPConnectionEstablisher import TCPConnectionEstablisher

class TestPort(IPPort):

    host = ''

    def broadcast(self):
        self.write(str(self.host) + ':' + str(self.acceptPort))
        self.flush()

    def newConnectedConnection(self, sock):
        sock = SocketStream(sock)
        sock = CachingStringStream(sock, 1024)
        return sock

    def newFactory(self, stream):
        return ListingStream(stream)
        return DebugStream(ListingStream(stream), str(id(stream)%100//4))


class ListingStream(Stream):

    def __init__(self, stream):
        Stream.__init__(self, stream)
        self._overtake_attribute('write')
        self._overtake_attribute('close')
        self._overtake_attribute('flush')
        self._overtake_attribute('update')
        self._overtake_attribute('readline')
        self._overtake_attribute('readlines')
        self._overtake_attribute('writelines')

    def read(self, *args):
        return [self.stream.read(*args)]
    

class test_IPPort(unittest.TestCase):

    def setUp(self):
        self.pl = []

    def newPort(self):
        p = TestPort()
        self.pl.append(p)
        return p

    def tearDown(self):
        for p in self.pl:
            p.close()

    def test_create(self):
        p = self.newPort()
        p.close()

    def test_open(self):
        p = self.newPort()
        p.open()
        p.close()
    
    def test_open_close_open(self):
        p = self.newPort()
        p.open()
        p.close()
        p.open()
    
    def do_broadcast(self):
        p = self.newPort()
        p.open()
        p.broadcast()
        time.sleep(0.01)
        return p

    def test_broadcast(self):
        p = self.do_broadcast()
        return p

    def test_broadcast_recv(self):
        p = self.test_broadcast()
        p.update()
        l = p.read()
        self.assertNotEqual([''], l)
        return p, l[0]

    def test_broadcast_recv_connect(self):
        p, s = self.test_broadcast_recv()
        host, port = s.split(':')
        if not host:
            host = 'localhost'
        e = TCPConnectionEstablisher((host, port))
        e.update()
        l = e.read(1)
        self.assertNotEqual([], l)
        time.sleep(0.001)
        return p, l[0]

    def test_broadcast_recv_connect_send(self):
        p, s = self.test_broadcast_recv_connect()
        p.update()
        l = p.read(1)
        self.assertNotEqual([''], l)
        self.assertEqual(2, len(l))
        s2 = l[(l.index('') + 1 ) % 2]
        s1 = CachingStringStream(SocketStream(s), 1024)
        s1.write('juhu')
        s1.flush()
        s2.update()
        self.assertEqual('juhu', s2.read())
        

if __name__ == '__main__':
    unittest.main(exit = None, verbosity = 1)

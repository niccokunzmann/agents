

from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw
from stream.IPPort import IPPort

debug = True

class test_build_cluster(unittest.TestCase):

##    @unittest.skip('todo')
    def test_dedicated_launch(self):
        port = IPPort()
        ps = launchDedicatedTest('test_built_cluster_dedicated.py', \
                    'test_built_cluster_dedicated.test_send_manager')
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
                l.extend(port.read())
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

    def build_sock(self):
        # listener
        lis = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # reuse addr
        lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lis.bind(('localhost', 0))
        port = lis.getsockname()[1]
        sndr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sndr.connect(('localhost', port))
        return sndr, lis
    
    def test_select_send_recv_udp_socket(self):
        sndr, lis = self.build_sock()
        sndr.send('hallo')        
        rl, wl, xl = select.select([lis], [], [], 1)
        self.assertNotEqual(rl, [])
        self.assertEqual('hallo', rl[0].recv(8096))
##    @unittest.skip('todo')
    def test_select_read_udp_socket_stream(self):
        sndr, lis = self.build_sock()
        sndr.send('hallo2')
        rd = css.CachingStringStream(sw.SocketStream(lis))
        rl, wl, xl = select.select([rd], [], [], 1)
        self.assertNotEqual(rl, [])
        rl[0].update()
        self.assertEqual('hallo2', rl[0].read())
        
    def test_select_read_write_udp_socket_stream(self):
        sndr, lis = self.build_sock()
        wd = css.CachingStringStream(sw.SocketStream(sndr))
        rd = css.CachingStringStream(sw.SocketStream(lis))
        wd.write("what's up")
        wd.flush()
        rl, wl, xl = select.select([rd], [], [], 1)
        self.assertNotEqual(rl, [])
        rd.update()
        self.assertEquals("what's up", rd.read())
        
    def test_select_accept(self):
        s = socket.socket()
        s2 = socket.socket()
        s.bind(('localhost', 0))
        s.listen(1)
        s2.connect(('localhost', s.getsockname()[1]))
        rl, wl, xl = select.select([s], [s], [s], 0)
        self.assertNotEqual([], rl)
        self.assertEqual([], wl)
        self.assertEqual([], xl)
        self.assertIs(s, rl[0])
        s.setblocking(0)
        s3, addr = s.accept()

    def test_reuse_addr_udp(self):
        sock1 = self.new_udp_sock()
        sock2 = self.new_udp_sock()

    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_reuse_addr_udp_ipv6(self):
        sock1 = self.new_udp_sock()
        sock2 = self.new_udp_sock()

        
    def new_udp_sock(self, family=socket.AF_INET, host=('localhost', 44055)):
        sock = socket.socket(family, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(host)
        return sock
        



if __name__ == '__main__':
    unittest.main(exit = False)

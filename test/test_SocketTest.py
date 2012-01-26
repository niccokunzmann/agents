
from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw

debug = True

PORT = 1

class test_SocketTest(unittest.TestCase):

    def build_sock(self):
        # listener
        lis = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # reuse addr
        lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lis.bind(('localhost', 0))
        port = lis.getsockname()[PORT]
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
        s2.connect(('localhost', s.getsockname()[PORT]))
        time.sleep(0.01)
        rl, wl, xl = select.select([s], [s], [s], 0)
        self.assertNotEqual([], rl, 'not connected')
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
        
    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    @unittest.expectedFailure
    def test_udp_v4_tov6(self):
        sock4 = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.udp_test(sock4, sock6)
        
    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    @unittest.expectedFailure
    def test_udp_v6_tov4(self):
        sock4 = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.udp_test(sock6, sock4)
        
    def udp_test(self, send, recv):
        recv.bind(('localhost', 0))
        send.connect(('localhost', recv.getsockname()[PORT]))
        send.send('laue winde')
        time.sleep(0.004)
        r = select.select([recv], [], [], 0)[0]
        self.assertNotEqual([], r, 'send does not work')
        r = r[0]
        self.assertEqual(recv, r)
        self.assertEqual('laue winde', r.recv(1024))
        
    def test_udp_v4_tov4(self):
        sock4 = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_test(sock6, sock4)

    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_udp_v6_tov6(self):
        sock4 = socket.socket(socket.AF_INET6 , socket.SOCK_DGRAM)
        sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.udp_test(sock6, sock4)

    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_tcp_v6_to_ipv4(self):
        sock4 = socket.socket(socket.AF_INET)
        sock6 = socket.socket(socket.AF_INET6)
        self.assertRaises(socket.error, self.tcp_test, sock6, sock4)
    
    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_tcp_v6_to_ipv6(self):
        sock4 = socket.socket(socket.AF_INET6)
        sock6 = socket.socket(socket.AF_INET6)
        self.tcp_test(sock4, sock6)
    
    def test_tcp_v4_to_ipv4(self):
        sock4 = socket.socket(socket.AF_INET)
        sock6 = socket.socket(socket.AF_INET)
        self.tcp_test(sock4, sock6)
    
    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_tcp_v4_to_ipv6(self):
        sock4 = socket.socket(socket.AF_INET)
        sock6 = socket.socket(socket.AF_INET6)
        self.assertRaises(socket.error, self.tcp_test, sock6, sock4)
        
    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_equal_bind(self):
        sock4 = socket.socket(socket.AF_INET)
        sock6 = socket.socket(socket.AF_INET6)
        sock4.bind(('localhost', 0))
        sock6.bind(('localhost', sock4.getsockname()[PORT]))
    
    def tcp_test(self, acc, conn):
        acc.bind(('localhost', 0))
        acc.listen(1)
        conn.connect(('localhost', acc.getsockname()[PORT]))

    def test_bind_dgram_socket(self):
        s = socket.socket()
        s.bind(('localhost', 0))
        s.listen(1)
        s2 = socket.socket(type = socket.SOCK_DGRAM)
        s2.bind(('localhost', s.getsockname()[PORT]))

    def test_send_from_bound_port(self):
        s2 = socket.socket(type = socket.SOCK_DGRAM)
        s2.bind(('localhost', 0))
        s3 = socket.socket(type = socket.SOCK_DGRAM)
        s3.bind(('localhost', 0))
        s2.sendto('hello', ('localhost', s3.getsockname()[PORT]))
        msg, addr = s3.recvfrom(64)
        self.assertEqual('hello', msg)
        self.assertEqual(s2.getsockname()[PORT], addr[PORT])

    def test_ipv4_broadcast(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast(s)

    @unittest.skipUnless(socket.has_ipv6, 'no ipv6 -> no test')
    def test_ipv6_broadcast(self):
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.broadcast(s, 'ff02::1')
        
    def broadcast(self, sock, addr = '<broadcast>'):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto('hallo!', (addr, 1234))
        

if __name__ == '__main__':
    unittest.main(exit = False)


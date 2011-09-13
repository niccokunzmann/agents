

from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw


class test_build_cluster(unittest.TestCase):

    @unittest.skip('todo')
    def test_dedicated_launch(self):
        port = IpPort()
        ps = launchDedicatedTest('test_built_cluster_dedicated', \
                    'test_built_cluster_dedicated.test_send_manager')
        ps.update()
        started = ps.read()
        self.assertIsTrue(started)
        port.broadcast()
        while 1:
            port.update()
            m = port.read()
            if m:
                break
        m.connect()
        m.write('hallo!')
        m.flush()
        m.update()
        message = m.read(1)
        self.assertEqual(['hello!'], message)

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
        



if __name__ == '__main__':
    unittest.main(exit = False)

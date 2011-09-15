from test import *


from stream.TCPConnectionEstablisher import *

import socket

PORT = 1

class test_TCPConnectionEstablisher(unittest.TestCase):

    def new(self, addr, *connections):
        return TCPConnectionEstablisher(addr, connections)

    def test_estab_con(self, fam = socket.AF_INET):
        s = socket.socket()
        s.bind(('localhost', 0))
        s.listen(1)
        e = self.new(s.getsockname())
        e.update()
        c1 = e.read()
        self.assertNotEqual([], c1)
        c1 = c1[0]
        c2, addr = s.accept()
        c1.send('hallo!')
        l = []
        c2.setblocking(0)
        doTimeout(lambda : (l.append(c2.recv(6)), 1/len(l)),
                  ZeroDivisionError, socket.error)
        self.assertEqual(['hallo!'], l)

    def test_estab_con_6(self):
        self.test_estab_con(socket.AF_INET6)

    def test_addrinfo(self):
        e = self.new(('localhost', 12))
        self.assertEqual(('localhost', 12), e.address_info)

    def test_other_con(self):
        e = self.new(('localhoat', 63784), 0,1,2,3)
        for i in range(4):
            e.update()
            self.assertEqual([i], e.read())
        self.assertRaises(socket.error, e.update)

    def test_factory(self):
        e = test_factory(self, self.new(('localhost', 234)))
        self.assertEqual(('localhost', 234), e.address_info)
if __name__ == '__main__':
    unittest.main(exit = None)

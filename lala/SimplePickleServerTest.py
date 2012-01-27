

import unittest
import SimplePickleServer
import RemoteTestCase
import socket
import random


class SimplePickleServerStartTest(unittest.TestCase):

    def setUp(self):
        self.server_addresses = []

    def tearDown(self):
        for address in self.server_addresses:
            SimplePickleServer.closeDedicatedServer(address)

    def test_start_onPort(self):
        self.startOnAddr(('127.0.0.1', random.randint(10000, 60000)))

    def test_start_on_abitrary_port(self):
        self.startOnAddr(('127.0.0.1', 0))

    def startOnAddr(self, addr):
        self.server_address = server_address = SimplePickleServer.startDedicatedServer(addr)
        self.server_addresses.append(server_address)
        self.assertNotEqual(self.addr[1], 0)
        if addr[1] != 0:
            self.assertEqual(self.addr[1], addr[1])
        self.assetEqual(self.addr[1], addr[1])
        return server_address

    
if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

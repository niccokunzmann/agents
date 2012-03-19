

import unittest
import SimplePickleServer
import RemoteTestCase
import socket
import random
import thread
import time

from SimplePickleServerController import closeDedicatedServer, startDedicatedServer

class SimplePickleServerBaseTestCase(unittest.TestCase):
    
    def setUp(self):
        self.server_addresses = []

    def tearDown(self):
        for address in self.server_addresses:
            closeDedicatedServer(address)


    def startOnAddr(self, addr):
        self.server_address = server_address = startDedicatedServer(addr)
        self.server_addresses.append(server_address)
        self.assertNotEqual(server_address[1], 0)
        if addr[1] != 0:
            self.assertEquals(server_address[1], addr[1])
        self.assertEquals(server_address[0], addr[0], 'host names are the same')
        return server_address

class SimplePickleServerStartTest(SimplePickleServerBaseTestCase):

    serverCloseTime = 0.3
    serverCloseTimeMore = 6

    def test_start_onPort(self):
        self.startOnAddr(('127.0.0.1', random.randint(10000, 60000)))

    def test_start_on_abitrary_port(self):
        self.startOnAddr(('127.0.0.1', 0))

    def start_server(self):
        return self.startOnAddr(('127.0.0.1', 0))

    def test_server_closes(self):
        addr = self.start_server()
        closeDedicatedServer(addr)
        def fails_with_socket_error():
            time.sleep(self.serverCloseTime)
            RemoteTestCase.createPickleConnection(addr, timeout = 1)
        self.assertRaises(socket.error, fails_with_socket_error)

    def test_server_closes_after_some_more_time(self):
        addr = self.start_server()
        time.sleep(self.serverCloseTimeMore)
        closeDedicatedServer(addr)
        def fails_with_socket_error():
            time.sleep(self.serverCloseTime)
            RemoteTestCase.createPickleConnection(addr, timeout = 1)
        self.assertRaises(socket.error, fails_with_socket_error)

    def test_server_can_be_closed_locally(self):
        server = SimplePickleServer.SimplePickleServer(('127.0.0.1', 0), \
                        SimplePickleServer.PickleRequestHandler)
        closed = []
        _server_close = server.server_close
        def server_close():
            _server_close()
            closed.append(1)
        server.server_close = server_close
        port = server.server_address[1]
        thread.start_new(server.serve_forever, ())
        closeDedicatedServer(('127.0.0.1', port))
        time.sleep(self.serverCloseTime)
        self.assertEquals(closed, [1], 'the server is closed')

class MockSimplePickleServer(object):
    closed = False
    def server_close(self):
        self.closed = True

class PatchedPickleRequastHandler(SimplePickleServer.PickleRequestHandler):

    
    def handle(self):
        # patch the handle function so the thread does not block
        pass

    def handle2(self):
        SimplePickleServer.PickleRequestHandler.handle(self)

    def finish(self):
        pass

    def finish2(self):
        SimplePickleServer.PickleRequestHandler.finish(self)

class PickleRequestHandlerTest(unittest.TestCase):

    # socketTransferTime is the time a socket transfer of bytes should last
    # from one andpoint on the local machine to another
    socketTransferTime = 0.1

    def setUp(self):
        self.server = server = MockSimplePickleServer()
        s = socket.socket()
        s.bind(('localhost', 0))
        s.listen(1)
        self.toHandler = RemoteTestCase.createPickleConnection(\
            s.getsockname())
        self.serversock = s.accept()[0]
        self.handler = PatchedPickleRequastHandler(\
            self.serversock, \
            self.serversock.getpeername(), \
            server)

    def tearDown(self):
        self.handler.finish2()

    def test_handler_closes_server(self):
        self.toHandler.write('shutdown')
        self.toHandler.flush()
        time.sleep(self.socketTransferTime)
        self.assertEquals(self.handler.handleOneRequest(), 'break')
        self.assertTrue(self.server.closed)

    def test_handler_closes_handler(self):
        self.toHandler.write('close')
        self.toHandler.flush()
        time.sleep(self.socketTransferTime)
        self.assertEquals(self.handler.handleOneRequest(), 'break')
        self.assertFalse(self.server.closed)

class ServerFunctionalityTest(SimplePickleServerBaseTestCase):

    HOST = 'localhost'

    def setUp(self):
        super(self).setUp()
        self.startOnAddr((self.HOST, 0))
        self.objectStream = SimpleSocketServer.createPickleConnection(\
            self.server_address)

    def tearDown(self):
        super(self).tearDown()
        self.objectStream.close()
        
    
if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

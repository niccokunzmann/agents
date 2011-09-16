
from Port import *

import socket

PORT = 1
ADDR = 0

from ConnectionFactory import DefaultConnectionFactoryFactory
from MultiStream import MultiStream
from SocketBroadcastStream import SocketBroadcastStream
from Connection import Connection
from CachingStringStream import CachingStringStream
from StreamWrap import SocketStream, WrapReadFactory
from SocketAcceptStream import SocketAcceptStream
from TCPConnectionEstablisher import TCPConnectionEstablisher

class IPPort(Port):

    ipv6 = socket.has_ipv6

    host = ''

    port = 6327

    broadcast_adresses = (('<broadcast>', 6327),('ff02::1', 6327))

    address_families = [socket.AF_INET]
    if socket.has_ipv6:
        address_families.append(socket.AF_INET6)

    def __init__(self):
        '''create a new IPPort
the factory constructor must take a stream of string
'''
        Port.__init__(self, None)
        self.connectionPort = None
        self._acceptStream = None
        self._broadcastStream = None
        self._broadcastReceiver = None
        self.broadcast_addresses = list(self.broadcast_adresses)
        self._connectionBuffer = []
        self.acceptPort = 0

    def _newFactory(self, *args):
        '''apply the arguments to the factory constructor and return the value'''
        raise NotImplementedError('implement this to use the factory')
        
    def open(self, port = None):
        '''open this port for reading and writing,
build new streams from sockets
the optimal port argument is preferred before the port attribute
and countains the port number of udp  sockets listening
port does not influence the port number for accepting connecions'''
        self.openBroadcastSend()
        self.openBroadcastReceive(port)
        self.openAccept()

    def openBroadcastSend(self):
        '''open the port for broadcasting'''
        if self._broadcastStream:
            raise ValueError('first disconnect to open for broadcasting')
        sockets = []
        for fam in self.address_families:
            s = socket.socket(fam, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sockets.append(s)
        broadcastStream = SocketBroadcastStream(sockets, \
                                                self.broadcast_addresses)
        broadcastStream = CachingStringStream(broadcastStream)
        broadcastStream = self._newFactory(broadcastStream)
        self._broadcastStream = broadcastStream

    def openBroadcastReceive(self, port = None):
        '''open the port for receiving broadcasts
for ore information about port see open(port)'''
        if self._broadcastReceiver:
            raise ValueError('first disconnect to open for receiving')
        if port is not None:
            self.port = port
        sockStreams = []
        buf = -1
        for fam in self.address_families:
            s = socket.socket(fam, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            buf = max((buf, s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
            s = SocketStream(s)
            sockStreams.append(s)
        broadcastReceiver = MultiStream(sockStreams)
        broadcastReceiver = CachingStringStream(broadcastReceiver, buf)
        broadcastReceiver = self._newFactory(broadcastReceiver)
        self._broadcastReceiver = broadcastReceiver

    def openAccept(self):
        '''open the port for acception connections'''
        if self._acceptStream:
            raise ValueError('first disconnect to open for accepting')
        sockets = []
        self.acceptPort = 0
        for fam in self.address_families:
            s = socket.socket(fam, socket.SOCK_STREAM)
            s.bind((self.host, self.acceptPort))
            s.listen(1)
            self.acceptPort = s.getsockname()[PORT]
            sockets.append(s)
        acceptStream = SocketAcceptStream(sockets)
        self._acceptStream = acceptStream

    def close(self):
        '''close the port'''
        self.closeBroadcastSend()
        self.closeBroadcastReceive()
        self.closeAccept()
    def closeBroadcastSend(self):
        '''close the port for broadcasting'''
        if self._broadcastStream:
            self._broadcastStream.close()
            self._broadcastStream = None
    def closeBroadcastReceive(self):
        '''close the port for receiving broadcasts'''
        if self._broadcastReceiver:
            self._broadcastReceiver.close()
            self._broadcastReceiver = None
    def closeAccept(self):
        '''close the port for accepting connections'''
        if self._acceptStream:
            self._acceptStream.close()
            self._acceptStream = None

    def read(self, count = -1):
        '''read objects from the port'''
        r = []
        while not (len(r) >- count > -1) and self._connectionBuffer:
            r.append(self._connectionBuffer.pop(0))
        if count == -1:
            l = self._broadcastReceiver.read()
        else:
            l = self._broadcastReceiver.read(count - len(r))
        r.extend(l)
        return r

    def update(self):
        '''update this port input'''
        self._broadcastReceiver.update()
        self._acceptStream.update()
        new_connections = self._acceptStream.read()
        for con in new_connections:
            con = self._newConnectedConnection(con)
            self._connectionBuffer.append(con)

    def _newConnectedConnection(self, socket):
        '''return a connection object for the given connected socket'''
        raise NotImplementedError('implement this to use the factory')

    def write(self, obj):
        '''mark objects to be sent other ports'''
        self._broadcastStream.write(obj)

    def flush(self):
        '''send the objects to other ports'''
        self._broadcastStream.flush()

    def broadcast(self):
        '''broadcast connection information'''
        self._getBroadcastConnection(self)
        self.write(conn)
        self.flush()

    def _getBroadcastConnection(self):
        '''return the connection information to broadcast'''
        raise NotImplementedError('implement this to use broadcast')
    

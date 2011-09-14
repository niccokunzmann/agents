

from Port import *

import StreamFactory
import StringStream
from CachingStringStream import CachingStringStream

import PickleStream

import StreamWrap

import socket
import select

from Connection import Connection


class SocketAcceptStream(Stream):

    def __init__(self, sockets, maxcon = -1):
        Stream.__init__(self, sockets)
        self.sockets = sockets
        self._buffer = []
        self.maxcon = maxcon

    def update(self):
        a = select.select(self.sockets, [], [], 0)[0]
        while a and not (len(self._buffer) > self.maxcon > -1):
            for sock in a:
                new_s, addr = sock.accept()
                self._buffer.append(new_s)
            a = select.select(self.sockets, [], [], 0)

    def read(self, count = -1):
        if count == -1:
            count = len(self._buffer)
        
        r = self._buffer[:count]
        self._buffer = self._buffer[count:]
        return r

SOCKET_CONNECTION_REFUSED_ERROR_CODE = (10061,)

class TCPSocketStream(Connection):

    connection_information_flags = (socket.SOL_TCP,)

    def __init__(self, host, port, connect = False, args = ()):
        self.host = host
        self.port = port
        self.args = args
        if connect:
            self.connect()

    def connect(self):
        con_info = self.getConnectionInformation(self)
        for con_spec in con_info:
            try:
                conn = self.establishConnectionTo(con_spec[:3], con_spec[4])
            except socket.error as e:
                if e[0] in SOCKET_CONNECTION_REFUSED_ERROR_CODE:
                    continue
                raise
            else:
                self.connectTo(conn)
                break

    def getConnectionInformation(self):
        args = self.args + (0,0)[:2 - len(self.args)]
        if len(args) < 3: # no flags
            args += self.connection_information_flags
        return socket.getaddrinfo(self.host, self.port, 0, 0, *args)

    def establishConnectionTo(self, sockargs, addr):
        s = socket.socket(*sockargs)
        s.connect(addr)
        return StreamWrap.SocketStream(s)

StreamFactory.registerStream(TCPSocketStream, None, \
                lambda s: (s.host, s.port, True, s.args))
        
class EndlessPacketStream(Stream):
    def __init__(self, packet = ''):
        Stream.__init__(self, packet)

    def read(self, size = None):
        return self.stream

    def update(self):
        pass

    def flush(self):
        pass

    def write(self, s):
        self.stream+= s

StreamFactory.registerStream(EndlessPacketStream, None, \
                             StreamFactory.streamArguments)

class IPConnection(Connection):

    def __init__(self, factory):
        Connection.__init__(self)
        self.factory = factory

    def connect(self):
        if not self.isConnected():
            self.factory.update()
            self.connectTo(self.factory.read())
            

def _toTuple(con):
    f = EndlessPacketStream()
    f = CachingStringStream(s)
    f = IPConnectionFactory(s)
    f.write(con.stream)
    f.flush()
    return f

StreamFactory.registerStream(IPConnection, None, _toTuple)

class IPConnectionFactory(StreamFactory.StreamFactory):

    def __init__(self, stream):
        StreamFactory.StreamFactory.__init__(self, stream)
        self.registerStream(BrokenStream.BrokenStream)
        self.registerStream(StringStream.StringStream)
        self.registerStream(CachingStringStream)
        self.registerStream(IPConnection)
        self.registerStream(TCPSocketStream)
        self.registerStream(EndlessPacketStream)
        self.registerStream(PickleStream.PickleStream)
        self.registerStream(type(self))

StreamFactory.registerStream(IPConnectionFactory, None, \
                             StreamFactory.streamArguments)

class BroadcastFactory(StreamFactory.StreamFactory):
    def __init__(self, stream):
        StreamFactory.StreamFactory.__init__(self, stream)
        self.registerStream(CachingStringStream)
        self.registerStream(EndlessPacketStream)
        self.registerStream(IPConnectionFactory)
    

class MultiStreamWriter(Stream):

    def __init__(self, streams):
        Stream.__init__(self, streams)

    def write(self, obj):
        for stream in self.stream:
            stream.write(obj)

    def flush(self):
        for stream in self.stream:
            stream.flush()

class IPPort(Port):

    DEFAULT_PORT = 6329

    broadcastAddrs = ['<broadcast>']

    def __init__(self, host = '', port = None):
        if port is None:
            port = self.DEFAULT_PORT
        self.port = port
        self.host = ''
        self._acceptStream = self._newAcceptStream()
        self._broadcastStream = self._newBroadcastStream()
        self._udpStream = self._newUdpStream()

    def _newAcceptStream(self):
        l = []
        s4 = socket.socket(socket.AF_INET)
        s4.bind((self.host, self.port))
        s4.listen(1)
        l.append(s4)
        if socket.has_ipv6:
            s6 = socket.socket(socket.AF_INET6)
            s6.bind((self.host, self.port))
            s6.listen(1)
            l.append(s6)
        a = SocketAcceptStream(l, 10)
        a = CachingStringStream(a)
        a = BroadcastFactory(a)
        return a

    def _newBroadcastStream(self):
        l = []
        l.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        if socket.has_ipv6:
            pass
##            l.append(socket.socket(socket.AF_INET6, socket.SOCK_DGRAM))
        for sock in l:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            for addr in self.broadcastAddrs:
                sock.connect((addr, self.port))
        m = MultiStreamWriter(l)
        return self.newUdpFactory(m)

    def newUdpFactory(self, stream):
        m = CachingStringStream(stream)
        m = BroadcastFactory(m)
        return m

    def newUdpStream(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        # todo
        


    def read(self, count = -1):
        return [IPConnection(sock) for sock in self._acceptStream.read(count)]

    def update(self):
        self._acceptStream.update()

    def write(self, obj):
        self._broadcastStream.write(obj)

    def flush(self):
        self._broadcastStream.flush()

    def broadcast(self):
        t = TCPSocketStream(self.host, self.port)
        c = CachingStringStream(t)
        p = PickleStream.PickleStream(c)
        i = IPConnection(p)
        self.write(i)
        self.flush()
        

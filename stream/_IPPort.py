

from Port import *

import StreamFactory
from StringStream import StringStream
from BrokenStream import BrokenStream
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
        while a and not (len(self._buffer) >= self.maxcon > -1):
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
SOCKET_OPERATION_NOT_SUPPORTED_ERROR_CODE = (10045,)

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
    s = EndlessPacketStream() # to reconnect
    s = CachingStringStream(s)
    f = IPConnectionFactory(s)
    f.write(con.stream)
    f.flush()
    return f

StreamFactory.registerStream(IPConnection, None, _toTuple)

class IPConnectionFactory(StreamFactory.StreamFactory):

    def __init__(self, stream):
        StreamFactory.StreamFactory.__init__(self, stream)
        self.registerStream(BrokenStream)
        self.registerStream(StringStream)
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
        self.registerStream(IPConnection)

class EstablishedIpConnection(Connection):
    def __init__(self, connection):
        Connection.__init__(self, connection)

    def connect(self):
        self.connectTo(self.stream)    

class ConnectionStream(Stream):

    def update(self):
        self.stream.update()

    def flush(self):
        self.stream.flush()

    def read(self, *args):
        return [self.wrapConnection(con) for con in self.stream.read(*args)]

    def wrapConnection(self, con):
        con = FileStream(con)
        con = PickleSteam(con)
        con = EstablishedIpConnection(con)
        return con

class MultiStream(Stream):

    def __init__(self, streams):
        Stream.__init__(self, streams)

    def write(self, obj):
        for stream in self.stream:
            stream.write(obj)

    def flush(self):
        for stream in self.stream:
            stream.flush()

    def read(self, count):
        rd, wt, x = select.select(self.stream, [], [], 0)
        if rd:
            return rd[0].read(count)
        return ''

    def update(self):
        pass

    def close(self):
        for stream in self.stream:
            stream.close()

def empty(*args, **kw):
    '''this function does nothing'''
    pass

class IPPort(Port):
    ''' A port for ip connections

broadcastAddrs: [...] of
    ((family, [type, [proto]]), hostname, port or None)
    if port is None it will be all of broadcastPorts
broadcastPorts
    the ports to broadcast to and to bind to
connectionPorts
    ports connections are accepted at
'''


    broadcastAddrs = [((socket.AF_INET, socket.SOCK_DGRAM), '<broadcast>', None), \
                      ((socket.AF_INET6, socket.SOCK_DGRAM),'ff02::1', None)]

    broadcastPorts  = (6328,)
    connectionPorts = (6329,)
    hosts = ('',)

    def __init__(self, hosts = None, broadcastPorts = None, \
                 connectionPorts = None, broadcastAddrs = None):
        if broadcastPorts is None:
            broadcastPorts = self.broadcastPorts
        self.broadcastPorts = broadcastPorts[:]
        if connectionPorts is None:
            connectionPorts = self.connectionPorts
        self.connectionPorts = connectionPorts[:]
        if broadcastAddrs is None:
            broadcastAddrs = self.broadcastAddrs
        self.broadcastAddrs = broadcastAddrs[:]
        if hosts is None:
            hosts = self.hosts
        self.hosts = hosts[:]
        self._closed = False
        
        self._acceptStream = self._newAcceptStream()
        self._broadcastStream = self._newBroadcastStream()

    def _newAcceptStream(self):
        l = []
        for port in self.connectionPorts:
            for host in self.hosts:
                accept_socket = self._newSocket(None, socket.SOCK_STREAM)
                accept_socket.bind((host, port))
                accept_socket.listen(1)
                l.append(accept_socket)
        a = SocketAcceptStream(l, 10)
        a = self.newEndpointFactory(a)
        return a

    def _newBroadcastStream(self):
        l = []
        for sockopt, addr, port in self.broadcastAddrs:
            if port:
                ports = (port,)
            else:
                ports = self.broadcastPorts
            for port in ports:
                sock = self._newSocket(*sockopt)
                if not port:
                    port = self.broadcastPorts
                sock.connect((addr, port))
                l.append(StreamWrap.SocketStream(sock))
        l.extend(self._newUdpPorts())
        m = MultiStream(l)
        return self.newBroadcastFactory(m)

    def _newUdpPorts(self):
        l = []
        for port in self.broadcastPorts:
            for host in self.hosts:
                sock = self._newSocket(None, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((host, port))
                s = StreamWrap.SocketStream(sock)
                import DebugStream
                s = DebugStream.DebugStream(s)
                s.write = empty
                l.append(s)
        return l
    
    def newBroadcastFactory(self, stream, bufsize = 8192):
        m = CachingStringStream(stream, bufsize)
        m = BroadcastFactory(m)
        return m

    def newEndpointFactory(self, stream, bufsize = 8192):
        m = ConnectionStream(stream)
        return m

    def _newSocket(self, family = None, type = None, proto = None):
        choose = family is None
        if choose:
            if socket.has_ipv6:
                family = socket.AF_INET6 # can handle also IPv4
            else:
                family = socket.AF_INET
        if type is None:
            type = socket.SOCK_STREAM
        if proto is None:
            args = (family, type)
        else:
            args = (family, type, proto)
        errors = (socket.error,) * choose
        try:
            return socket.socket(*args)
        except errors: # cannot create IPv6 socket
            return self._newSocket(socket.AF_INET, type, proto)
        
    def read(self, count = -1):
        r = []
        l = self._acceptStream.read(count)
        if not (len(l) >= count > -1):
            e = self._broadcastStream.read(1)
            r.extend(e)
        for sock in l:
            s = StreamWrap.SocketStream(sock)
            f = self.newBroadcastFactory(s)
            c = IpConnection(f)
            r.append(c)	
        return r

    def update(self):
        self._acceptStream.update()
        self._broadcastStream.update()

    def write(self, obj):
        self._broadcastStream.write(obj)

    def flush(self):
        self._broadcastStream.flush()

    def broadcast(self):
        '''broadcast a remote connection'''
        con = self.createRemoteConnection()
        self.write(con)
        self.flush()

    def createRemoteConnection(self):
        '''create an unconnected remote connection'''
        t = TCPSocketStream(socket.gethostname(), self.connectionPorts[0])
        c = CachingStringStream(t)
        p = PickleStream.PickleStream(c)
        return IPConnection(p)
        

    def close(self):
        s = getattr(self, '_acceptStream', None)
        if s:
            s.close()
        s = getattr(self, '_broadcastStream', None)
        if s:
            s.close()
        self._closed = True

    def __del__(self):
        if not self._closed:
            self.close()

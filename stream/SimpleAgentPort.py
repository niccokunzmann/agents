
from IPPort import IPPort

from SimpleAgent import SimpleAgent

from Stream import Stream
from StreamWrap import SocketStream
from FileStream import FileStream
from PickleStream import PickleStream
from FactoryConnection import FactoryConnection
from TCPConnectionEstablisher import TCPConnectionEstablisher

import StreamFactory
import socket

PORT = 1
ADDR = 0

class SimpleAgentPort(IPPort):
    '''This is a'''

    agentClasses = [SimpleAgent]

    def __init__(self, agent):
        '''create a new SimpleAgentPort
all received connections'''
        IPPort.__init__(self)
        self._agent = agent

    def _getBroadcastConnection(self):
        '''return the connection information to broadcast'''
        addr = self.getConnectAddress()
        if addr[PORT] is None:
            raise ValueError('the portmust accept connections to broadcast')
        factory = TCPConnectionEstablisher(addr)
        factory = SimpleAgentStreamBuilder(factory)
        conn = SimpleAgentPortConnection(self._agent, addr, factory)
        return conn

    def _newConnectedConnection(self, sock):
        '''create a new socket connection wrap'''
        return self._broadcastStream._wrapSocket(sock)

    def _newFactory(self, stream):
        '''return a new Factory to use'''
        factory = SimpleAgentConnectionFactory(stream)
        for agentClass in self.agentClasses:
            factory.registerStream(agentClass)
        return factory

    def getfqdn(self):
        '''return the fully qualified name for this host'''
        return socket.getfqdn(self.host)

    def getConnectAddress(self):
        return (self.getfqdn(), self.acceptPort)
        

class SimpleAgentStreamBuilder(Stream):

    def __init__(self, stream):
        Stream.__init__(self, stream)

    def read(self, *count):
        socks = self.stream.read(*count)
        return [self._wrapSocket(sock) for sock in socks]

    def update(self):
        self.stream.update()

    def close(self):
        self.stream.close()

    @staticmethod
    def _wrapSocket(sock):
        sock = SocketStream(sock)
        sock = FileStream(sock)
        # todo: add stream caching more and better -> faster read 
        sock = PickleStream(sock)
        return sock
        
StreamFactory.registerStream(SimpleAgentStreamBuilder, None, \
                             StreamFactory.streamArguments)

class SimpleAgentConnectionFactory(StreamFactory.StreamFactory):
    SteamBuilder = SimpleAgentStreamBuilder
    def __init__(self, stream, connections = ()):
        StreamFactory.StreamFactory.__init__(self, stream)
        self.connections = connections
        self.register()

    def register(self):
        self.registerNewStream(TCPConnectionEstablisher, None, \
                               self._connectionEstablisherToTuple, \
                               self._connectionEstablisherFromTuple)
        self.registerStream(self.SteamBuilder)
        self.registerStream(SimpleAgentPortConnection)

    @staticmethod
    def _connectionEstablisherToTuple(e):
        return (e.address_info,)
    def _connectionEstablisherFromTuple(self, addr_info):
        return TCPConnectionEstablisher(addr_info, self.connections)

    @staticmethod
    def _wrapSocket(sock):
        return self.StreamBuilder._wrapSocket(sock)
        


class SimpleAgentPortConnection(FactoryConnection):
    def __init__(self, agent, address, factory):
        FactoryConnection.__init__(self, factory)
        self.agent = agent
        self.address = address

    def connectTo(self, stream):
        # todo: agent receives connection?
        FactoryConnection.connectTo(self, stream)

    def toTuple(self):
        return self.agent, self.address, self.factory

StreamFactory.registerStream(SimpleAgentPortConnection, None, \
                             lambda c: c.toTuple())

class OneStreamFactory(Stream):
    def __init__(self, stream):
        Stream.__init__(self, stream)

    def read(self, count = None):
        stream = self.stream
        if stream is None:
            return []
        self.stream = None
        return stream

    def update(self):
        pass

    def close(self):
        pass

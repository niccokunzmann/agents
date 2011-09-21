

import socket
import select

from IPPort import IPPort

from Stream import Stream
from StreamWrap import SocketStream, WrapReadFactory, forList
from FileStream import FileStream
from SimpleAgent import SimpleAgent
from DebugStream import DebugStream
from PickleStream import PickleStream
from FactoryConnection import FactoryConnection
from TCPConnectionEstablisher import TCPConnectionEstablisher

import StreamFactory



PORT = 1
ADDR = 0



class UpdateStream(FileStream):
    ''' this stream calls update until everything is read
this requires the underlying string to have the fileno() function implemented
if this is not the case update will be called only once
pay attention that there will be read from the stream, too
otherwise this may walk into an endless loop
'''

    def __init__(self, stream, maxUpdates = -1):
        ignore = []
        if hasattr(stream, 'fileno'):
            ignore.append('update')
            self._maxUpdates = maxUpdates
        FileStream.__init__(self, stream, ignore = ignore)

    def update(self):
        '''update the stream as often as possible'''
        s = select.select([self.stream], [], [], 0)[0]
        m = self._maxUpdates
        while s and (m == -1 or m >= 1):
            self.stream.update()
            s = select.select([self.stream], [], [], 0)[0]
            m -= 1


class TCPSocketStreamWrapper(WrapReadFactory):
    '''wrap a SocketStream around each read'''

    def __init__(self, stream):
        WrapReadFactory.__init__(self, stream, forList(SocketStream))

StreamFactory.registerStream(TCPSocketStreamWrapper)

class OneReadStream(Stream):
    '''this stream returns [stream] once and then []'''
    def __init__(self, stream):
        Stream.__init__(self, stream)

    def read(self, count = None):
        stream = self.stream
        if stream is None:
            return []
        self.stream = None
        return [stream]

    def update(self):
        pass

    def close(self):
        pass


class SimpleAgentStreamBuilder(WrapReadFactory):
    '''this builds a PickleStream around each value read'''

    def __init__(self, stream):
        WrapReadFactory.__init__(self, stream, forList(self._wrapStream))

    @staticmethod
    def _wrapStream(stream):
        stream = FileStream(stream)
        # todo: add stream caching more and better -> faster read
        stream = PickleStream(stream)
        stream = UpdateStream(stream)
        return stream
        
StreamFactory.registerStream(SimpleAgentStreamBuilder)

class SimpleAgentPortConnection(FactoryConnection):
    def __init__(self, agent, address, builder):
        FactoryConnection.__init__(self, builder)
        self.agent = agent
        self.address = address

    def connectTo(self, stream):
        # todo: agent receives connection?
        FactoryConnection.connectTo(self, stream)

    def toTuple(self):
        return self.agent, self.address, self.factory

StreamFactory.registerStream(SimpleAgentPortConnection, None, \
                             lambda c: c.toTuple())

class SimpleAgentPort(IPPort):
    '''This is a SimpleAgentPort

Register
    a list of classes to register for reading and writing
    to read different Agent classes put them here
    also Builder for different stream connections can be put to here
    they will also be accepted by the factory
    and may be broadcasted by other ports to specify connections

Builder
    this builder builds new incoming connections
    it will be broadcastet to other ports to enable connections to them

Factory
    the factory writes builder classes to the broadcast
    it also receives broadcasts and reads builders and connections

Connection
    the connection class that will be read by other ports
    it represents the connection to this port
    it is called by _newConnection like Connection(agent, address, builder)


if you want to costomize the creation of the builder or a new connection or
another factory overrride _newBuilder(stream), _newConnection(stream)
and _newFactory and donnot forget to place the used streams in Register 
when replacing _newFactory please add all streams in Register



'''

    Register = [SimpleAgent, TCPSocketStreamWrapper, TCPConnectionEstablisher, \
                FileStream, SimpleAgentPortConnection]
    Builder = SimpleAgentStreamBuilder
    Factory = StreamFactory.StreamFactory
    Connection = SimpleAgentPortConnection

    def __init__(self, agent):
        '''create a new SimpleAgentPort
the agent is the agent all connections will be addressed to and
should inherit from SimpleAgent'''
        IPPort.__init__(self)
        self._agent = agent

    def _getBroadcastConnection(self):
        '''return the connection information to broadcast'''
        addr = self.getConnectAddress()
        builder = TCPConnectionEstablisher(addr)
        builder = TCPSocketStreamWrapper(builder)
        builder = self._newBuilder(builder)
        conn = self._newConnection(builder)
        return conn

    def _newConnection(self, builder):
        '''return a new connection to this port around the stream'''
        addr = self.getConnectAddress()
        connection = SimpleAgentPortConnection(self._agent, addr, builder)
        return connection
        
    def _newConnectedConnection(self, sock):
        '''create a new socket connection wrap'''
        stream = OneReadStream(sock)
##        stream = DebugStream(stream, 'newCon')
        stream = TCPSocketStreamWrapper(stream)
        builder = self._newBuilder(stream)
        connection = self._newConnection(builder)
        return connection

    def _newFactory(self, stream):
        '''return a new Factory to use'''
        factory = self.Factory(stream)
        for cls in self.Register:
            factory.registerStream(cls)
        factory.registerStream(self.Builder)
        return factory

    def _newBuilder(self, stream):
        '''return a new bulder'''
        stream = FileStream(stream)
        return self.Builder(stream)


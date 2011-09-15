
from Stream import Stream
from IPPort import IPPort
from Connection import Connection
from TCPConnectionEstablisher import TCPConnectionEstablisher
from StreamWrap import WrapReadFactory, SocketStream
from FactoryConnection import FactoryConnection
from CachingStringStream import CachingStringStream
from EndlessStringStream import EndlessStringStream
from DebugStream import DebugStream

import socket

PORT = 1
HOST = 0

class StringPort(IPPort):
    
    def broadcast(self):
        if not self.acceptPort:
            raise ValueError('openAccept before broadcasting')
        host = socket.getfqdn()
        self.write((host, self.acceptPort))
        self.flush()

    def newConnectedConnection(self, sock):
        buf = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        peername = sock.getpeername()
##        sock = DebugStream(SocketStream(sock), 'conn%i'%(id(sock)//4%25))
        sock = SocketStream(sock)
        sock = CachingStringStream(sock, 1024)
        sock = EndlessConnectionFactory(sock)
        sock = StringPortConnection(sock, (peername[HOST], 0))
        return sock

    def newFactory(self, stream):
        return StringConnectionFactory(stream)

class EndlessConnectionFactory(EndlessStringStream):
    pass

class StringConnectionFactory(Stream):

    def __init__(self, stream):
        Stream.__init__(self, stream)
        self._overtake_attribute('flush')
        self._overtake_attribute('update')
        self._overtake_attribute('fileno')
        self._overtake_attribute('close')

    def write(self, addr):
        if type(addr) is tuple:
            host = addr[0]
            port = addr[1]
            self.stream.write(host)
            self.stream.write(':' + str(port))
            self.stream.write('\n')
        elif hasattr(addr, 'getPeerAddr'):
            addr = addr.getPeerAddr()
            self.write(addr)
        else:
            raise ValueError('only address tuples or objects with getPeerAddr()'\
                             ' are supported')

    def read(self, count = 1):
        if not count:
            return []
        line = self.stream.readline()
        host, port = line.strip().rsplit(':', 1)
        address = (host, int(port))
        factory = TCPConnectionEstablisher(address)
        factory = WrapReadFactory(factory, self._wrapRead)
        stream = StringPortConnection(factory, address)
        return [stream]

    def _wrapRead(self, socks):
        return [self._wrapReadSock(sock) for sock in socks]

    def _wrapReadSock(self, s):
##        s = DebugStream(SocketStream(s), 'sock%i'%(id(s)//4%25))
        s = SocketStream(s)
        s = CachingStringStream(s)
        return s
        
class StringPortConnection(FactoryConnection):
    '''This is a connection only for StringPort'''
    def __init__(self, factory, address):
        self.address = address
        FactoryConnection.__init__(self, factory)
        
    def getPeerAddr(self):
        '''return the address of the peer'''
        return self.address



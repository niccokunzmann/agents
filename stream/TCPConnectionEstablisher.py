
from Stream import *

import sys
import socket

import StreamFactory


if socket.has_ipv6:
    TCPSOCK_ARGS = (socket.AF_INET6, socket.SOCK_STREAM)
else:
    TCPSOCK_ARGS = (socket.AF_INET, socket.SOCK_STREAM)
    

class TCPConnectionEstablisher(Stream):

    def __init__(self, address_info, connections = ()):
        self._connection_iter = iter(connections)
        Stream.__init__(self, None)
        self.address_info = address_info

    def update(self):
        '''load new connection'''
        if self.stream is not None:
            return 
        for connection in self._connection_iter:
            self.stream = connection
            break
        else:
            addr_info  = socket.getaddrinfo(*self.address_info)
            ty = None
            for family, type, proto, canonname, addr in addr_info:
                sock = socket.socket(family, type, proto)
                try:
                    sock.connect(addr)
                except socket.error:
                    ty, er, tb = sys.exc_info()
                    self.stream = None
                    continue
                self.stream = sock
                return
            if ty is not None:
                raise ty, ty(*(er.args + (str(addr_info),))), tb
                

    def read(self, count = 1):
        '''get a new connection'''
        if self.stream is None:
            return []
        r = self.stream
        self.stream = None
        return [r]

StreamFactory.registerStream(TCPConnectionEstablisher, None, \
                             lambda e: (e.address_info[:2],))

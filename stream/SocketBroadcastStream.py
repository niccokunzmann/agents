
from Stream import *

import socket

class SocketBroadcastStream(Stream):

    def __init__(self, sockets, addresses):
        '''take a list'''
        self.sockets = sockets
        for sock in sockets:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.addresses = addresses
        Stream.__init__(self, None)


    def write(self, string):
        '''send the stream immediately to the addresses
the string is sent once for each address'''
        addrs = list(self.addresses)
        socks = list(self.sockets)
        for sock in socks:
            for addr in addrs[:]:
                try:
                    sock.sendto(string, addr)
                    addrs.remove(addr)
                except socket.error:
                    pass

    def flush(self):
        '''flush does nothing since write does the work'''
        pass


    def close(self):
        '''close the sockets'''
        for sock in self.sockets:
            sock.close()

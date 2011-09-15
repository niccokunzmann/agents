
from Stream import *

import socket
import select


class SocketAcceptStream(Stream):

    def __init__(self, sockets, maxcon = -1):
        Stream.__init__(self, sockets)
        self.sockets = sockets
        self._buffer = []
        self.maxcon = maxcon

    def update(self):
        '''buffer all new connections'''
        a = select.select(self.sockets, [], [], 0)[0]
        while a and not (len(self._buffer) >= self.maxcon > -1):
            for sock in a:
                new_s, addr = sock.accept()
                self._buffer.append(new_s)
            a = select.select(self.sockets, [], [], 0)[0]

    def read(self, count = -1):
        '''read new connections from the buffer'''
        if count == -1:
            count = len(self._buffer)
        r = self._buffer[:count]
        self._buffer = self._buffer[count:]
        return r

    def close(self):
        '''close all sockets'''
        for sock in self.sockets:
            sock.close()

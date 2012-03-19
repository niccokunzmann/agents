import sys
import subprocess
import re
import select
import socket

from pickleConnection import createPickleConnection

import SimplePickleServer

class ControllerError(Exception):
    pass

class ServerCrashed(ControllerError):
    pass

class SimplePickleServerController(object):
    '''This is a controller fo a SimplePickleServer

it can start the server, close it and create connections to the server
'''

    def __init__(self, address = ('127.0.0.1', 0)):
        self.address = address
        self.started = False
        self.process = None

    def start(self):
        'start a server \n' \
        '=> (host, port)'
        if self.started:
            raise ControllerError('The server is already started. close it first.')
        self.started = True
        address = self.address
        executable = sys.executable
        if executable.lower().endswith('w.exe'):
            executable = executable[:-5] + executable[-4:]
        args = [executable, SimplePickleServer.__file__, \
                str(address[0]), str(address[1])]
        p = subprocess.Popen(args,
                             stdout = subprocess.PIPE, \
                             stdin = subprocess.PIPE, \
                             stderr = subprocess.PIPE, \
                             )
        line = p.stdout.readline()
        try:
            host, port = line.rstrip().split(' ')[-1].rsplit(':')
        except:
            raise ValueError('cannot exctract host:port from %r' % line)
        self.process = p
        self.address = host, int(port)
        return self.address

    def _createConnection(self, *args, **kw):
        return createPickleConnection(self.address, *args, **kw)
    
    def getConnection(self, *args, **kw):
        return self._createConnection(*args, **kw)

    def closeProcessIO(self):
        if self.process:
            self.process.stdin.close()
            self.process.stderr.close()
            self.process.stdout.close()
            self.process = None


    def shutdownServer(self, *args, **kw):
        'close a server'
        try:
            connection = self.getConnection(*args, **kw)
        except socket.error:
            ret = False # server is closed
        else:
            connection.write('shutdown')
            connection.close()
            ret = True
        self.started = False

    def close(self):
        self.closeProcessIO()
        self.shutdownServer()

    def stop(self):
        self.close()

def startDedicatedServer(*address):
    controller = SimplePickleServerController(*address)
    return controller.start()

def closeDedicatedServer(address, *args, **kw):
    'close a server'
    controller = SimplePickleServerController(address)
    return controller.close(*args, **kw)


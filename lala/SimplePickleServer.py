from SocketServer import ThreadingTCPServer, StreamRequestHandler
import cPickle
import traceback
import sys
import MeetingPlace
import os

from RemoteTestCase import wrapSocketForPickle, createPickleConnection

class PickleRequestHandler(StreamRequestHandler):
    def setup(self):
        StreamRequestHandler.setup(self)
        self.objectStream = wrapSocketForPickle(self.rfile)
        self.intoMeetingPlace()

    def intoMeetingPlace(self):
        MeetingPlace.setdefault('connections', dict())
        MeetingPlace.connections[self.client_address] = self.objectStream
        
    def handle(self):
        while 1:
            try:
                result = self.objectStream.read()
                if result == 'close':
                    break
                if result == 'shutdown':
                    self.server.close()
            except:
                traceback.print_exc()


def startDedicatedServer(address = ('127.0.0.1', 0)):
    'start a server \n' \
    '=> (host, port)'
    import subprocess
    import re

    assert os.path.isfile(sys.executable)
    assert os.path.isfile(__file__)
    print [sys.executable, __file__, \
                          str(address[0]), str(address[1])]
    p = subprocess.Popen([sys.executable],
                         stdout = subprocess.PIPE, \
##                         stdin = subprocess.PIPE, \
##                         shell = True, \
                         )
    host, port = p.stdout.readline().rstrip().split(' ')[-1].rsplit(':')
    return host, int(port)

def closeDedicatedServer(address, *args, **kw):
    'close a server'
    try:
        connection = RemoteTestCase.createPickleConnection(address, *args, **kw)
    except socket.error:
        return
    else:
        connection.write('shutdown')
        connection.close()


def main(argv = sys.argv, ServerClass = ThreadingTCPServer, \
         RequestHandlerClass = PickleRequestHandler):
    # evaluate host argument
    HOST = 'localhost'
    if len(argv) >= 2:
        HOST = argv[1]
    if HOST == 'all':
        HOST = ''
    if len(argv) >= 3:
        PORT = int(argv[2])
    else:
        PORT = 0

    server = ServerClass((HOST, PORT), RequestHandlerClass)
    print 'sever listening on %s:%i' % (HOST, server.server_address[1])

    MeetingPlace.setdefault('server', [])
    MeetingPlace.server.append(server)
    
    server.serve_forever()


if __name__ == '__main__':
    main()
    

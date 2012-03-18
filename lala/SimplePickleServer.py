from SocketServer import ThreadingTCPServer, StreamRequestHandler
import cPickle
import traceback
import sys
import MeetingPlace
import os
import socket

try:
    path = __file__
except NameError:
    pass
else:
    for i in range(2):
        path = os.path.split(path)[0]
        if not path:
            break
        sys.path.append(path)

from pickleConnection import wrapSocketForPickle, createPickleConnection

class SimplePickleServer(ThreadingTCPServer):

    def serve_forever(self):
        try:
            ThreadingTCPServer.serve_forever(self)
        except socket.error:
            # no error output if closed
            pass

class PickleRequestHandler(StreamRequestHandler):
    def setup(self):
        StreamRequestHandler.setup(self)
        self.objectStream = wrapSocketForPickle(self.connection)
        self.intoMeetingPlace()

    def intoMeetingPlace(self):
        MeetingPlace.setdefault('connections', dict())
        MeetingPlace.connections[self.client_address] = self.objectStream
        
    def handle(self):
        while 1:
            try:
                if self.handleOneRequest() == 'break':
                    break
            except:
                traceback.print_exc()

    def handleOneRequest(self):
        self.objectStream.update()
        result = self.objectStream.read()
        ret = None
        if 'close' in result:
            ret = 'break'
        if 'shutdown' in result:
            self.server.server_close()
            ret = 'break'
        return ret

def startDedicatedServer(address = ('127.0.0.1', 0)):
    'start a server \n' \
    '=> (host, port)'
    import subprocess
    import re
    import select
    executable = sys.executable
    if executable.lower().endswith('w.exe'):
        executable = executable[:-5] + executable[-4:]
    p = subprocess.Popen([executable, __file__, \
                          str(address[0]), str(address[1])],
                         stdout = subprocess.PIPE, \
                         stdin = subprocess.PIPE, \
                         stderr = subprocess.PIPE, \
                         )
    line = p.stdout.readline()
    host, port = line.rstrip().split(' ')[-1].rsplit(':')
    p.stdin.close()
    p.stderr.close()
    p.stdout.close()
    return host, int(port)

def closeDedicatedServer(address, *args, **kw):
    'close a server'
    try:
        connection = createPickleConnection(address, *args, **kw)
    except socket.error:
        return
    else:
        connection.write('shutdown')
        connection.close()


def main(argv = sys.argv, ServerClass = SimplePickleServer, \
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
    if HOST == '':
        HOST = 'all'
    print 'sever listening on %s:%i\r\n' % (HOST, server.server_address[1])
    sys.stdout.flush()

    MeetingPlace.setdefault('server', [])
    MeetingPlace.server.append(server)
    
    server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    finally:
        print
    

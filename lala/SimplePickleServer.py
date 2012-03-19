from SocketServer import ThreadingTCPServer, StreamRequestHandler

import traceback
import sys
import MeetingPlace
import os
import socket
import thread

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

from pickleConnection import wrapSocketForPickle

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
        MeetingPlace.setdefault('connections_by_threadid', dict())
        connection = self.objectStream
        MeetingPlace.connections[self.client_address] = connection
        MeetingPlace.last_connection = connection
        MeetingPlace.connections_by_threadid[thread.get_ident()] = connection
        
    def handle(self):
        while 1:
            try:
                if self.handleOneRequest() == 'break':
                    break
            except:
                traceback.print_exc()

    def handleOneRequest(self):
        try:
            self.objectStream.update()
            result = self.objectStream.read()
        except (socket.error, EOFError):
            return 'break'
        ret = None
        if 'close' in result:
            ret = 'break'
        if 'shutdown' in result:
            self.server.server_close()
            ret = 'break'
        return ret

    

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
        

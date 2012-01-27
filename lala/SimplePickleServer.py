from SocketServer import ThreadingTCPServer, StreamRequestHandler
import cPickle
import traceback
import sys
import MeetingPlace

class PickleRequestHandler(StreamRequestHandler):
    def setup(self):
        StreamRequestHandler.setup(self)
        self.objectReader = cPickle.Unpickler(self.rfile)
        
    def handle(self):
        while 1:
            try:
                if self.objectReader.load() == 'close':
                    break
            except:
                traceback.print_exc()


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
        PORT = 6326

    server = ServerClass((HOST, PORT), RequestHandlerClass)
    MeetingPlace.setdefault('server', [])
    MeetingPlace.server.append(server)
    server.serve_forever()


if __name__ == '__main__':
    main()
    

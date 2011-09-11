import sys
import os

import subprocess
import test
del test
from subprocess import PIPE

import socket
import time

from stream.PickleStream import PickleStream
from stream.StreamWrap import StdIOStream, SocketStream
from stream.FileStream import FileStream
from stream.DebugStream import DebugStream

import re


tests_succeded_regex = re.compile('(?s).*\nOK[^\n]*$')


class DedicatedTestStream(FileStream):

    def __init__(self, picklestream, pipe, name = ''):
        FileStream.__init__(self, picklestream)
        self.stderr = pipe.stderr
        self.stdout = pipe.stdout
        self.stdin  = pipe.stdin
        self.pipe = pipe
        self.__printed = False
        self.name = name

    def printOnFail(self):
        '''print the stderr to stderr if the tests did not succeed
return succeeded'''
        self.__printed = True
        stdout, stderr = self.pipe.communicate()
        if tests_succeded_regex.match(stderr) is None:
            sys.stderr.write("--------> error output starting for %s ------->\n" % self.name)
            sys.stderr.write(stderr)
            sys.stderr.write("<--------- error output ending for %s <--------\n" % self.name)
            if stdout:
                sys.stdout.write("--------> output starting for %s ------->\n" % self.name)
                sys.stdout.write(stdout)
                sys.stdout.write("<--------- output ending for %s <--------\n" % self.name)
            return False
        return True

    def noPrintOnFail(self):
        self.__printed = True

    def __del__(self):
        if not self.__printed:
            sys.stdout.write('%s object deleted without print' % self)

def launchDedicatedTest(filename, *tests):
    if not os.path.exists(filename):
        filename = os.path.join(os.path.split(sys.argv[0])[0], filename)
    s = socket.socket()
    s.bind(('localhost', 0))
    s.listen(1)
    s.setblocking(0)
    port = s.getsockname()[1]
##    print 'connection to port', port
    exe = sys.executable
    #exe = 'C:\\bin\\winpdb.bat'
    args = [exe, filename, str(port)]
    args.extend(list(tests))
    pipe = subprocess.Popen(args, stdin = PIPE,
                            stdout = PIPE, stderr = PIPE,
                            )
    sock, addr = doTimeout(s.accept, socket.error, default = (None, None))
    if sock is None:
        raise socket.error('connection refused')
##    print 'sock:', sock, sock.getpeername(), sock.getsockname()
    socketstream = (SocketStream(sock))
##    print 'socketstream:', socketstream
    picklestream = PickleStream(FileStream(socketstream))
    return DedicatedTestStream(picklestream, pipe, filename)

def beDedicatedTest():
    port = int(sys.argv.pop(1))
    sock = socket.socket()
    sock.connect(('localhost', port))
##    print 'sock:', sock, sock.getpeername(), sock.getsockname()
    socketstream = (SocketStream(sock))
    picklestream = PickleStream(FileStream(socketstream))
    return picklestream

TIMEOUT = 4

def doTimeout(function, *errors, **kw):
    timeout = TIMEOUT + time.time()
    while timeout > time.time():
        try:
            return function()
        except errors:
            pass
        time.sleep(0.01)
    return kw.get('default', None)


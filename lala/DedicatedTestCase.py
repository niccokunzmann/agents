
import thread
import socket
import time
import sys


import unittest

import SimplePickleServerController
from pickleConnection import wrapSocketForPickle, createPickleConnection
import distobj.objects.GlobalObject as GlobalObject


class DedicatedTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.controller = SimplePickleServerController.\
                         SimplePickleServerController(('localhost', 1234))
        cls.controller.start()

    @classmethod
    def tearDownClass(cls):
##        cls.controller.shutdownServer()
####        print 7
####        s = cls.controller.process.stderr.read(100000)
####        print 8
####        if s != ' ':
####            sys.stderr.write(s)
        cls.controller.close()
##        print 9

    def setUp(self):
        self.connection = self.controller.getConnection()
        self._runReadThread(self.connection)

    def tearDown(self):
        self.connection.write('break')
        self.connection.close()
        self.connection = None

    def _runReadThread(self, connection):
        thread.start_new(self._readThread, (connection,))

    def _readThread(self, connection):
        while connection == self.connection:
            try:
                connection.update()
            except (socket.error, EOFError):
                break

    def send(self, obj):
        self.connection.write(obj)
        self.connection.flush()

    def recv(self):
        return self.connection.read(1)[0]

TIMEOUT = 5

def doTimeout(function, *errors, **kw):
    '''doTimeout(function, error1, ..., default = None, timeout = TIMEOUT)
retry to call the function and return the value
call doTimeout(..., timeout = seconds, ...) to set the timeout
the timeout defaults to TIMEOUT
doTimeout(..., default = value, ...) determines the default return value
if the function did not succeed
'''
    tm = kw.get('timeout', TIMEOUT)
    timeout = tm + time.time()
    while timeout > time.time():
        try:
            return function()
        except errors:
            pass
        time.sleep(0.01)
    return kw.get('default', None)

        


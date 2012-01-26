
from Connection import *

class UnableToConnectError(ConnectionError):
    '''The stream is unable to connect'''
    pass




class FactoryConnection(Connection):

    def __init__(self, factory, stream = None):
        '''create a new connection
the factory as firt argument returns a new stream when calling read(1)'''
        self.factory = factory
        Connection.__init__(self, stream)

    def connect(self):
        '''connect to the stream returned by the factory'''
        if self.isConnected():
            raise ConnectedError('the connection has to be disconnected'\
                                 ' to connect again')
        self.factory.update()
        stream = self.factory.read(1)
        if type(stream) is list:
            if not stream:
                raise UnableToConnectError('cannot connect because nothing was'\
                                ' read from the factory %r' % self.factory)
            stream = stream[0]
        self.connectTo(stream)


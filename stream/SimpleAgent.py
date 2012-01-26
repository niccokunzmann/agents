
from FactoryConnection import FactoryConnection
from FactoryConnection import UnableToConnectError
from FactoryConnection import ConnectionError
from FactoryConnection import NotConnectedError


from distobj.objects.GlobalObject import GlobalObject
from MultiStreamReader import MultiStreamReader
from MultiStream import MultiStream

import StreamFactory

class SimpleAgent(GlobalObject, FactoryConnection):

    def __init__(self, name):
        FactoryConnection.__init__(self.default, \
                                   MultiStreamReader(), \
                                   MultiStream([]))

    def addConnectionFactory(self, factory):
        self.factory.addStream(factory)

    def connectTo(self, stream):
        '''add a stream to the streams'''
        self._connected = True
        self.stream.addStream(stream)

StreamFactory.registerStream(SimpleAgent, None, \
                             lambda a: (a.getName(),))



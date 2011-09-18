
from FactoryConnection import FactoryConnection
from FactoryConnection import UnableToConnectError
from FactoryConnection import ConnectionError
from FactoryConnection import NotConnectedError


from distobj.objects.GlobalObject import GlobalObject
from MultiStreamReader import MultiStreamReader

import StreamFactory

class SimpleAgent(GlobalObject, FactoryConnection):

    def __init__(self, name):
        # todo: add groups
        FactoryConnection.__init__(self.default, MultiStreamReader())

    def addConnectionFactory(self, factory):
        self.factory.addStream(factory)


StreamFactory.registerStream(SimpleAgent, None, \
                             lambda a: (a.getName(),))



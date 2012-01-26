from test import *

from stream.SimpleAgent import *

from test_GlobalObject import test_GlobalObject

from stream.Stream import Stream

class DummyFactory(Stream):
    def __init__(self):
        Stream.__init__(self, None)
        self.writes = 0
        self.reads  = 0
        self.flushes = 0
        self.updates = 0
    def read(self, count = None):
        self.reads+= 1
        return ['dum dudi dum'] * ((self.reads) % 5 != 0)

    def update(self):
        self.updates+= 1

    def write(self, value):
        self.writes+= 1
        self.value = value

    def flush(self):
        self.flushes+= 1

class test_SimpleAgent(test_GlobalObject):

    def newObject(self, name, *args):
        return SimpleAgent(name, *args)

    def test_dedicated_echo(self):
        m = self.newObject('test_dedicated_echo')
        m2 = dedicated_echo(m)
        self.assertIsNot(None, m2, 'echo failed')
        self.assertIs(m, m2)
        
    def test_dedicated(self):
        m = self.newObject('test_dedicated')
        ps = dedicated_echo


    def test_factory(self):
        test_factory(self, self.newObject('test_factory'))

    def test_add_factory(self, name = 'test_add_factory'):
        a = self.newObject(name)
        f = DummyFactory()
        a.addConnectionFactory(f)
        a.connect()
        self.assertEqual(a.stream, 'dum dudi dum')
        self.assertTrue(a.isConnected())
        return a

    def test_disconnect(self, name = 'test_disconnect'):
        a = self.test_add_factory(name)
        a.disconnect()
        self.assertRaises(NotConnectedError, a.write, 1)
        self.assertFalse(a.isConnected())

    def test_add_two_factories(self):
        # this test is highly dependent on MultiStreamReader
        a = self.newObject('test_add_two_factories')
        f1 = DummyFactory()
        a.addConnectionFactory(f1)
        a.addConnectionFactory(f1)
        self.assertEquals(1, len(a.factory.stream))
        f2 = DummyFactory()
        a.addConnectionFactory(f2)
        self.assertEquals(2, len(a.factory.stream))
        for i in range(24):
            a.connect()
            a.disconnect()
        self.assertRaises(UnableToConnectError, a.connect)
        
def test_module():
    unittest.main(exit = False, verbosity = 1)

if __name__ == '__main__':
    test_module()


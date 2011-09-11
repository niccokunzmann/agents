from test import *

from stream.Manager import Manager

from test_GlobalObject import test_GlobalObject

class test_Manager(test_GlobalObject):

    def newObject(self, name, *args):
        return Manager(name, *args)

    def test_dedicated_echo(self):
        m = self.newObject('test_dedicated_echo')
        m2 = dedicated_echo(m)
        self.assertIsNot(None, m2, 'echo failed')
        self.assertIs(m, m2)
        
    def test_dedicated(self):
        m = self.newObject('test_dedicated')
        ps = dedicated_echo






def test_module():
    unittest.main(exit = False, verbosity = 1)

if __name__ == '__main__':
    test_module()


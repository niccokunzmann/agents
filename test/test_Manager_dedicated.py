
from test import *

from test_Manager import Manager

class test_GlobalObject_dedicated(unittest.TestCase):

    def getObject(self, name, *args):
        return Manager(name, *args)


    def test_dedicated(self):
        
    




if __name__ == '__main__':
    ps = beDedicatedTest()
    unittest.main(exit = False)

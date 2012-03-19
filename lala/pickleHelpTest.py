import unittest
import pickle

from DedicatedTestCase import DedicatedTestCase, doTimeout
from pickleHelp import *

class packCodeTest(unittest.TestCase):

    def dump_and_load(self, obj):
        s = pickle.dumps(obj)
        return pickle.loads(s)

    def test_default_return_value(self):
        obj = packCode('', {'obj': 3})
        self.assertEquals(3, self.dump_and_load(obj))

    def test_return_value_set_in_code(self):
        obj = packCode('globals()["obj"] = 3', {})
        self.assertEquals(3, self.dump_and_load(obj))
       
    def test_code_executes_in_globals(self):
        obj = packCode('globals()["obj"] = xxx', {'xxx':5})
        self.assertEquals(5, self.dump_and_load(obj))

    def test_code_without_builtins(self):
        self.assertRaises(NameError, \
                lambda: self.dump_and_load(packCode('globals', {}, False)))


WAIT_FOR_RESPONE_TIMEOUT = 1

class connection_back_Test(DedicatedTestCase):

    def test_code_pings_back(self):
        self.send(packCode('''if 1:
        back.write('hallo')
        back.flush()''', dict(back = connection_back)))
        self.assertEquals(doTimeout(self.recv, Exception, \
                                    timeout = WAIT_FOR_RESPONE_TIMEOUT),\
                          'hallo')

if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

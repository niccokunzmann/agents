
from pickleConnecion import wrapSocketForPickle, createPickleConnection

import unittest


class RemoteTestCase(unittest.TestCase):

    def execute_dedicated(self, function):
        

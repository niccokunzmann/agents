
import sys
import time
import thread


from TestGlobalObject import TestGlobalObject

class HelloGreeting(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



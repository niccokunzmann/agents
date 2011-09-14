
from Connection import *
from distobj.objects.GlobalObject import *

from BrokenStream import BrokenStream



class Manager(GlobalObject, Connection):
    '''A Manager is both - a stream and a special Object'''

    def __init__(self, name):
        Connection.__init__(self.default, None)

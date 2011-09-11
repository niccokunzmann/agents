from GlobalObject import *

import thread



class Manager(GlobalObject):

    def __init__(self, name):
        pass


    def newConnection(self, newCon):
        self.connections.append(newCon)

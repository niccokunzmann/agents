
from GlobalObject import GlobalObject

import thread

class Group(GlobalObject):

    def __init__(self, name):
        '''create a new Group object'''
        if not self.default.__lock:
            self.default.__lock = thread.allocate_lock()
        self.default.__members = []

    def addMember(self, newMember):
        '''add a member to this group'''
        with self.__lock:
            if self.hasMember(newMember):
               self.__members.append(newMember)

    def getMembers(self):
        '''re turn a list of members of this group'''
        return self.__members[:]

    def hasMember(self, member):
        '''is member of this group? return a bool'''
        return member not in self.__members
        
    def isGroup(self):
        '''return True because the object is a group object'''
        return True

def isGroup(obj):
    '''return wether the given object is a Group object'''
    return hasattr(obj, 'isGroup') and obj.isGroup()

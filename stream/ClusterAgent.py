from SimpleAgent import SimpleAgent

from distobj.objects.Group import Group, isGroup

import thread

import StreamFactory

class ClusterAgent(SimpleAgent):

    def __init__(self, name, groups = []):
        SimpleAgent.__init__(self, name)
        if not self.default._lock:
            self.default._lock = thread.allocate_lock()
        self.default._groups = []
        for group in groups:
            self.joinGroup(group)

    def joinGroup(self, group):
        '''let the agent join the group'''
        if not isGroup(group):
            group = self._newGroup(group)
        group.addMember(self)
        with self._lock:
            if group not in self._groups:
                self._groups.append(group)

    def isMemberOf(self, group):
        '''return wether the agent is a member of the given group'''
        return group.hasMember(self)

    def _newGroup(self, name):
        '''return a new GroupObject for the agent to join'''
        return Group(name)

    def getGroups(self):
        '''return a list of groups the agent is in'''
        return self._groups[:]

    def newConnection(self, connection):
        '''handle a new connection
connect if the agent has at least one group in common
'''
        agent = connection.getAgent()
        if connection.isLocal():
            connection.connect()
        if agent != self:
            for group in self.getGroups():
                for group2 in agent.getGroups():
                    if group == group2:
                        connection.connect()
                        return

    def toTuple(self):
        '''used to broadcast the agent'''
        l = []
        for group in self.getGroups():
            l.append(group.getName())
        return self.getName(), tuple(l)

StreamFactory.registerStream(ClusterAgent, None, \
                             lambda a: a.toTuple())


from ClusterAgent import ClusterAgent, Group



class ClusterPart(object):
    '''
Ports
    a list of functions that will be called with the agent as first argument
    those functions shall return a Port instance or something alike
    what from connections can be read


'''
    Ports = []
    Agent = ClusterAgent
    
    def __init__(self, *args):
        self._agent = self._newAgent(*args)

    def _newAgent(self, *args):
        return self.Agent(*args)

    def getGroups(self):
        return self._agent.getGroups()

    def getName(self):
        return self._agent.getName()


    def close(self):
        '''close the cluster part'''
        pass


    

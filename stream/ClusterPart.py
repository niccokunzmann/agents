
from ClusterAgent import ClusterAgent, Group



class ClusterPart(object):
    '''

'''    
    def __init__(self, agent, ports = [], start = True):
        '''create a new ClusterPart object

ports
    a list of functions that will be called with the agent as first argument
    those functions shall return a Port instance or something alike
    what from connections can be read



'''
        self._agent = agent
        self._ports = []
        self.openPorts(ports)
        if start:
            self.start()

    def start(self):
        '''start parallel port updating'''

    def openPorts(self, ports = []):
        agent = self.getAgent()
        for Port in ports:
            port = Port(agent)
            port.open()
            self._ports.append(port)

    def getGroups(self):
        return self.getAgent().getGroups()

    def getName(self):
        return self.getAgent().getName()

    def getAgent(self):
        return self._agent

    def close(self):
        '''close the cluster part'''
        for port in self._ports:
            port.close()

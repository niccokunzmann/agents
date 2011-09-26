
from ClusterAgent import ClusterAgent, Group
from distobj.objects.Job import TimedJob
from SimpleAgentPort import SimpleAgentPort

class UpdatePortJob(TimedJob):
    '''UpdatePortJob
update the port and pass each new connection to newConnection(connection)
'''

    def __init__(self, port, newConnection, interval):
        TimedJob.__init__(self, interval)
        self.port = port
        self.newConnection = newConnection
        self.cons = []
        
    def do(self):
        self.giveNewConnections()
        self.port.update()
        self.cons.extend(self.port.read())
        self.giveNewConnections()

    def giveNewConnections(self):
        while self.cons:
            con = self.cons.pop()
            self.newConnection(con)


class ClusterIPPort(SimpleAgentPort):
    Register = SimpleAgentPort.Register + \
               [ClusterAgent]
    

class ClusterPart(object):
    '''

'''

    portUpdateInterval = 5
    portBroadcastInterval = 5
    
    def __init__(self, agent, ports = [], \
                 portUpdateInterval = None, \
                 portBroadcastInterval = None):
        '''create a new ClusterPart object

ports
    a list of functions that will be called with the agent as first argument
    those functions shall return a Port instance or something alike
    what from connections can be read

portUpdateInterval
    seconds after which the ports will all be updated
    set to -1 to disable receiving or to None to use default values

portBroadcastInterval
    seconds after wich the connection information will be broadcasted
    set to -1 to disable receiving or to None to use default values

'''
        self._agent = agent
        self._ports = []
        self._jobs = []
        if portUpdateInterval is None:
            self._portUpdateInterval = self.portUpdateInterval
        else:
            self._portUpdateInterval = portUpdateInterval
        if portBroadcastInterval is None:
            self._portBroadcastInterval = self.portBroadcastInterval
        else:
            self._portBroadcastInterval = portBroadcastInterval
        self.openPorts(ports)

    def openPorts(self, ports = [], portUpdateInterval = None):
        '''add and open the ports to read connections
the new connections will be passed to the agent
'''
        if portUpdateInterval is None:
            portUpdateInterval = self._portUpdateInterval
        agent = self.getAgent()
        for Port in ports:
            port = Port(agent)
            port.open()
            self._ports.append(port)
            if self._portUpdateInterval >= 0:
                ujob = UpdatePortJob(port, self.newConnection, \
                                                self._portUpdateInterval)
                self._jobs.append(ujob)
            if self._portBroadcastInterval >= 0:
                bjob = TimedJob(self._portBroadcastInterval, port.broadcast)
                self._jobs.append(bjob)

    def setMaxPortInterval(self, seconds):
        '''set the maximum interval to read connections from ports '''
        self._portUpdateInterval = seconds
        for job in self._jobs:
            if job.interval > seconds:
                job.interval = seconds

    def getJobs(self):
        '''return the jobs running to update and broadcast'''
        return self._jobs

    def newConnection(self, connection):
        self._agent.newConnection(connection)

    def getGroups(self):
        '''return the groups the agent is in'''
        return self.getAgent().getGroups()

    def getName(self):
        '''return the name of the agent'''
        return self.getAgent().getName()

    def getAgent(self):
        '''return the agent of this port'''
        return self._agent

    def close(self):
        '''close the cluster part'''
        for job in self._jobs:
            job.stop()
        for port in self._ports:
            port.close()


from ReplicatingObject import ReplicatingObject, R
import ReplicatingObject as ReplicatingObjectModule
import Agent as AgentModule


print 'lalala'


class ReducableRepresentation(object):
    def __init__(self, agent, function, args):
        self.agent = agent
        self.function = function
        self.args = args

    def __reduce__(self):
        referencedModules = self.getModulesReferencedByAgent()
##        referencedModules = \
##            self.getModulesReferencedbyClassModules(referencedModules)
        agentModules = self.selectPortableModules(referencedModules)
        replicatingObject = self.getReplicatingObjectForModules(agentModules)
        return replicatingObject.__reduce__()

    def getReducableFunction(self):
        return R(getattr, R(__import__, self.function.__module__), \
                        self.function.__name__)

    def getReturnObject(self):
        fct = self.getReducableFunction()
        return R(fct, *self.args)
    
    def getModulesReferencedByAgent(self):
        return [AgentModule, ReplicatingObjectModule]

    def selectPortableModules(self, modules):
        return modules

    def getReplicatingObjectForModules(self, modules):
        replicatingObject = ReplicatingObject()
        for module in modules:
            replicatingObject.addModuleDependency(module)
        replicatingObject.setReturnObject(self.getReturnObject())
        return replicatingObject

class Agent(object):

    def getInitArgs(self):
        return ()

    def getReducableRepresentation(self):
        return ReducableRepresentation(self, type(self), self.getInitArgs())
    
    def __reduce__(self):
        return self.getReducableRepresentation().__reduce__()

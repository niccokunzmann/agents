
import ReplicatingObject
import Agent as AgentModule




class Agent(object):

    def __reduce__(self):
        referencedModules = self.getModulesReferencedByAgent()
##        referencedModules = \
##            self.getModulesReferencedbyClassModules(referencedModules)
        agentModules = self.selectPortableModules(referencedModules)
        replicatingObject = self.getReplicatingObjectForModules(agentModules)
        return replicatingObject.__reduce__()


    __reduceAgent__ = object.__reduce__
    
    def getModulesReferencedByAgent(self):
        return [AgentModule, ReplicatingObject]

    def selectPortableModules(self, modules):
        return modules

    def getReplicatingObjectForModules(self, modules):
        replicatingObject = ReplicatingObject.ReplicatingObject()
        for module in modules:
            replicatingObject.addModuleDependency(module)
        replicatingObject.setReturnObject(self, '__reduceAgent__')
        return replicatingObject

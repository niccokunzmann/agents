'''This is the base module for Agents

see http://docs.python.org/library/pickle.html#the-pickle-protocol \n


'''


import ReplicatingObject
import sys

R = ReplicatingObject.R

class S(R):
    'this object reduces with a state\n'\
    '__reduce__() => (callable, args, state)'
    def __init__(self, state, *args):
        super(type(self), self).__init__(self, *args)
        self.rep += (state,)

class AgentReducer(object):
    'This class reduces Agents to a pickleable representation\n'\
    'see http://docs.python.org/library/pickle.html#the-pickle-protocol \n'\
    'for more information.\n'\
    
    def __init__(self, agent, callable):
        'initialize the reducable representation with the agent \n'\
        'and a callable that is called on the other side when deserializing\n'\
        'the callable usually is type(agent)\n'\
        'this callable should be a class or a function available in a module\n'\
        'no test is performed wether this callable exists now\n'\
        'because it may exist in the other program\n'
        self.agent = agent
        self.callable = callable

    def getReducableCallable(self):
        'return a reducable representation of the callable'
        callable = self.callable
        return R(getattr, R(__import__, callable.__module__), \
                          callable.__name__)

    def callOrRaiseOrDefault(self, funcname, default):
        'helper method to get optional pickle protocol functions:\n'\
        '\t__getstate__(), __getinitargs__()'
        func = getattr(self.agent, funcname, None)
        if func is None:
            return default
        if not callable(func):
            raise TypeError('%s of agent %s should be callable' % \
                            (funcname, self.agent))
        return func()

    def getReturnObject(self):
        'return the pickleable representation of the agent\n'\
        'this representation is returned by the unpickler'
        default = []
        arguments = self.callOrRaiseOrDefault('__getinitargs__', default)
        if arguments is default:
            arguments = ()
        state = self.callOrRaiseOrDefault('__getstate__', default)
        if state is default:
            return R(self.getReducableCallable(), *arguments)
        return S(self.getReducableCallable(), state, *arguments)

    def __reduce__(self):
        return self.getReturnObject().__reduce__()

class ModuleFinder(object):

    def __init__(self, agent):
        'this finder finds all modules the agent depends on'
        self.agent = agent
    
    def findModules(self):
        'return the modules referenced by agent and required for transition'
        referencedModules = self.getModulesReferencedByAgent()
##        referencedModules = \
##            self.getModulesReferencedbyClassModules(referencedModules)
        return self.selectPortableModules(referencedModules)

    def getModulesReferencedByAgent(self):
        '=> list of modules'
        modules = []
        map(modules.extend, \
            map(self.getRequiredModulesByClass, type(self.agent).mro()))
        return modules

    def getRequiredModulesByClass(self, cls):
        'type => list of modules'
        if cls == object:
            return []
        modules = cls.getRequiredModules()
        clsmod = cls.getModule()
        if clsmod is not None:
            modules.append(clsmod)
        return modules

    def selectPortableModules(self, modules):
        'list of modules => list of modules'
        return modules

    def getReplicatingObjectForModules(self, modules):
        '=> ReplicatingObject'
        self.removeDuplicates(modules)
        replicatingObject = ReplicatingObject()
        for module in modules:
            replicatingObject.addModuleDependency(module)
        replicatingObject.setReturnObject(self.getReturnObject())
        return replicatingObject

    @staticmethod
    def removeDuplicates(list):
        'remove duplicates from a list'
        list.sort(key = id)
        i = 1
        while i < len(list):
            while list[i] == list[i - 1]:
                list.pop(i)
            i += 1
        return list

class Agent(object):
    ModuleFinderClass = ModuleFinder
    AgentReducerClass = AgentReducer
        
    @classmethod
    def getRequiredModules(cls):
        return []

    @classmethod
    def getModule(cls):
        'return the module the class is in\n'\
        'be careful when overwriting this - subclasses will inherit\n'\
        'to add new required modules overwrite getRequiredModues()\n'\
        'if the module this class is in is not required\n'\
        'return None'
        mod = __import__(cls.__module__)
        if getattr(mod, cls.__name__, None) == cls:
            return mod
        for attrName in cls.__dict__:
            attr = getattr(cls, attrName, None)
            attr = getattr(attr, 'im_func', attr) # get the attribute
            if hasattr(attr, 'func_globals'):
                if attr.func_globals[cls.__name__] == cls:
                    glob = attr.func_globals
                    if '__loader__' in glob and \
                       hasattr(glob['__loader__'], 'get_module'):
                        print 'ja!'
                        return glob['__loader__'].get_module(cls.__module__)
        return mod

    @classmethod
    def getRequiredModules(cls):
        'get the modules required for this class to transit\n'\
        ''
        return []

    def __getinitargs__(self):
        'return the arguments the class is initialized with'
        return ()

    def getReducableRepresentation(self):
        'return the object that will handle __reduce__()\n'\
        'and return the agent afterwards'
        replicatingObject = ReplicatingObject.ReplicatingObject()
        for module in self.requiredModules():
            replicatingObject.addModuleDependency(module)
        replicatingObject.setReturnObject(self.getReturnObject())
        return replicatingObject

    def requiredModules(self):
        'return te modules required and referenced by this agent'
        return self.ModuleFinderClass(self).findModules()

    def getReturnObject(self):
        'return a reducable representation of this agent'
        return self.AgentReducerClass(self, type(self))
    
    def __reduce__(self):
        'return the reduced reducable representation of this agent'
        r = self.getReducableRepresentation()
        return r.__reduce__()

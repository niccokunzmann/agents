
import sys
import linecache
import types

class UnknownModuleError(ImportError):
    pass

class ThisShallNeverBeCalledError(Exception):
    pass

class R(object):
	def __init__(self, f, *args):
		self.ret = (f, args)
	def __reduce__(self):
		return self.ret
	def __call__(self, *args):
		raise ThisShallNeverBeCalledError()

class ReplicatingObject(object):

    def __init__(self):
        self.modules = {} # module name : lines
        self.addModuleDependency(__import__(__name__))

    def addModuleDependency(self, module):
        moduleKey = self.getModuleKey(module)
        self.modules[moduleKey] = self.getModuleEntry(module))

    def getModuleEntry(self, module):
        return linecache.getlines(module.__file__, module.__dict__)

    def hasModuleDependency(self, module):
        return self.getModuleKey(module) in self.modules

    def getModuleKey(self, module):
        if self.isModule(module):
            return module.__name__
        raise ValueError('expected module but got %s of type %s' % \
                         (module, type(module).__name__))

    def isModule(self, module):
        return isinstance(module, types.ModuleType)

    def getReplicationCode(self):
        return '''
locals().update(__import__(__import__.__module__).__dict__)
##global __builtins__
__builtins__ = vars(__import__('__builtin__'))

types = __import__('types')

loadedModules = {} # name : Module

class Loader(object):
    def __init__(self, source):
        self.source = source

    def get_source(self):
        return self.source

    

def _import(name, *args, **kw):
    global __builtins__
    print '_import:', name, args, kw
    __builtins__ = __import__('__builtin__')
    if name in loadedModules:
        return loadedModules[name]
    if name in modules:
        return loadModule(name)
    return __import__(name, *args, **kw)

def loadModule(module):
    global __builtins__
    __builtins__ = __import__('__builtin__')
    mod = types.ModuleType(module)
    mod.__builtins__ = __builtins__
    mod.__name__ = module
    mod.__import__ = _import
    code = compile(''.join(modules[module]), 'file:' + module, 'exec')
    exec code in vars(mod)
    return mod

for module in modules:
    print 'loading:', module, modules[module]
    loadModule(module)

obj = None
'''
        

    def __reduce__(self):
        code = self.getReplicationCode()
        globalVars = dict(
            code = code,
            __import__ = __import__,
            modules = self.modules,
            locals = locals)
        
        # get the function type
        FunctionType = R(type, R(eval, 'lambda:None'))
        # get the compilation code
        code = R(compile, code, __name__ + '.getReplicationCode()', 'exec')
        # the final object that can reduce, dump and load itself
        obj = R(R(getattr, tuple, '__getitem__'), (
                R(R(FunctionType, code, globalVars)),
                R(R(getattr, globalVars, 'pop'), 'obj')
                ), -1)
        return obj.__reduce__()
    

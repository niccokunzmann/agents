
import sys
import  os
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

__defaultObject = object()

class ReplicatingObject(object):

    def __init__(self):
        self.modules = {} # module name : lines
        self.addModuleDependency(__import__(__name__))

    def addModuleDependency(self, module):
        moduleKey = self.getModuleKey(module)
        self.modules[moduleKey] = self.getModuleEntry(module)

    def addCodeDependency(self, code, codeName, locals = {}, **kw):
        kw.update(locals)
        self.modules[codeName] = [code, codeName, kw]

    def getModuleEntry(self, module):
        filepath = module.__file__
        if filepath.lower().endswith('.pyc'):
            filepath = filepath[:-1]
        if not os.path.isfile(filepath):
            filepath += 'w' # .pyw files
        return [''.join(linecache.getlines(filepath, module.__dict__)), \
                module.__name__,
                dict(__package__ = getattr(module, '__package__'),
                     __file__ = module.__file__)]

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
sys = __import__('sys')
weakref = __import__('weakref')

loadedModules = {} # name : Module


class GlobalsImporter(object):

    def __init__(self):
        self.fullNames = weakref.WeakValueDictionary()

    def find_module(self, fullname, path = None):
##        print 'find_module:', fullname, path
##        print self.fullNames.keys()
        loader = self.fullNames.get(fullname, None)
        if loader is not None and loader.acceptImportInModule():
            return loader
        return None

    def checkForDelete(self):
        for fullname in self.fullNames:
            if self.fullNames.has_key(fullname):
                return
        self.delete()

    def addLoader(self, fullname, loader):
        self.fullNames[fullname] = loader

    def delete(self):
        'this removes the object from sys.meta_path'
        sys.meta_path.remove(self)

    def __eq__(self, other):
        return type(self).__name__ == type(other).__name__

globalsImporter = GlobalsImporter()

for importer in sys.meta_path[:]:
    if hasattr(importer, 'checkForDelete'):
        importer.checkForDelete()
sys.meta_path.append(globalsImporter)


class Loader(object):
    def __init__(self, source, fullname, moduleVars):
        self.__dict__.update(locals())
        self.loaded = False
        self.module = types.ModuleType(fullname)
        self.canBeLoaded = True

    def load_module(self, fullname):
        self.assertCanLoad(fullname)
        if self.loaded: # fix: race condition
            return self.module
        self.loaded = True
        self.executeModule(self.module)
        return self.module

    def acceptImportInModule(self):
        return self.canBeLoaded

    def assertCanLoad(self, fullname):
        if fullname != self.fullname:
            raise ValueError('can only import %s but should import %s' % \
                             (self.fullname, fullname))

    def executeModule(self, module):
##        print 'executeModule:', self.fullname
        module.__builtins__ = __builtins__
        module.__loader__ = self
        module.__dict__.update(self.moduleVars)
        code = compile(self.source, self.filename, 'exec')
        exec code in module.__dict__

    def get_source(self, fullname):
        self.assertCanLoad(fullname)
        return self.source
    get_data = get_source
    def get_code(self, fullname):
        return compile(self.get_source(fullname), self.filename, 'exec')
    def get_filename(self):
        return self.filename

    @property
    def filename(self):
        return self.moduleVars.get('__file__', '<>')

    def __eq__(self, other):
        return type(self) == type(other)

    def delete(self):
        self.canBeLoaded = False

loaders = []

for moduleName in modules:
    loader = Loader(*modules[moduleName])
    loaders.append(loader)
    globalsImporter.addLoader(moduleName, loader)

for loader in loaders:
    loader.load_module(loader.fullname)

del loader
del loaders # donnot drop weak references till the end

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

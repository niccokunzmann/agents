
import os
import unittest 
import linecache

from cPickle import loads, dumps

import ReplicatingObject

import MeetingPlace

class ReplicatedObjectBaseTest(unittest.TestCase):

    def setUp(self):
        self.rep = ReplicatingObject.ReplicatingObject()

    def dump_and_load(self):
        return loads(dumps(self.rep))


class ReplicatedObjectTest(ReplicatedObjectBaseTest):

    def test_compiles_without_warning(self):
        self.rep.getReplicationCode()

    def test_dump(self):
        dumps(self.rep)

    def test_dump_load(self):
        self.dump_and_load()

    def test_has_module_as_dependent(self):
        import os
        self.rep.addModuleDependency(os)
        self.assertTrue(self.rep.hasModuleDependency(os))

class MockReplicatingObject(ReplicatingObject.ReplicatingObject):

    def setReplicationCode(self, code):
        self.__replication_code = code

    def getReplicationCode(self):
        return self.__replication_code


class ReplictionCodeTest(ReplicatedObjectBaseTest):

    def setUp(self):
        MeetingPlace.loaded = 0
        self.rep = MockReplicatingObject()

    def test_loaded_after_dump_and_load(self):
        self.rep.setReplicationCode('''if 1:
            MeetingPlace = __import__('MeetingPlace')
            MeetingPlace.loaded = 1
            obj = None''')
        self.dump_and_load()
        self.assertEquals(MeetingPlace.loaded, 1)

    def test_modules_are_transferred_no_modules(self):
        self.assertModulesDumpedAndLoaded({})

    def test_modules_are_transferred_a_test_list(self):
        self.assertModulesDumpedAndLoaded([1,2,3])

    def assertModulesDumpedAndLoaded(self, modules):
        self.rep.modules = modules
        self.rep.setReplicationCode('''if 1:
            obj = modules''')
        modulesDumpedAndLoaded = self.dump_and_load()
        self.assertEquals(modulesDumpedAndLoaded, modules)

class ModuleLoaderTest(ReplicatedObjectBaseTest):

    def setUp(self):
        self.rep = ReplicatingObject.ReplicatingObject()
        import MeetingPlace
        MeetingPlace.loadedModules = []

    def addCache(self, name, code):
        moduleName = 'cache.' + name
        filename =  os.path.join('cache', name + '.py')
        f = file(filename, 'w')
        f.write(code)
        f.close()
        linecache.updatecache(filename)
        return moduleName

    def dump_and_load_as_module(self, name, code):
        moduleName = self.addCache(name, code)
        self.rep.addModuleDependency(__import__(moduleName))
        return self.dump_and_load()
        
    def test_load_someModule(self):
        someModule = '''if 1:
            import MeetingPlace
            MeetingPlace.loadedModules.append('someModule')'''
        self.dump_and_load_as_module('someModule', someModule)
        import MeetingPlace
        self.assertIn('someModule', MeetingPlace.loadedModules)

    def test_cache_modules_can_be_imported(self):
        code = '#emptyModule'
        self.addCache('emptyModule', code)
        import cache.emptyModule

    def test_lines_of_cache_modules_in_linecache(self):
        code = '#this is a line\n#andthisanother\na = 1\n'
        self.addCache('lineTest', code)
        import cache.lineTest
        self.assertEquals(linecache.getlines(cache.lineTest.__file__),
                          code.splitlines(True))


    def test_load_several_modules(self):
        moduleN = '''if 1:
            import MeetingPlace
            MeetingPlace.loadedModules.append(__name__)'''
        baseName = 'module%s'
        number_of_modules = 5
        moduleNames = []
        for i in range(number_of_modules):
            name = baseName % i
            moduleName = self.addCache(name, moduleN)
            moduleNames.append(moduleName)
            module = self.importModuleByName(moduleName)
            self.rep.addModuleDependency(module)
        self.assertAllModulesLoaded(moduleNames)
        MeetingPlace.loadedModules = []
        self.dump_and_load()
        self.assertAllModulesLoaded(moduleNames)

    def assertAllModulesLoaded(self, moduleNames):
        self.assertEquals(len(MeetingPlace.loadedModules), len(moduleNames))
        self.assertModulesLoaded(moduleNames)

    def assertModulesLoaded(self, moduleNames):
        for moduleName in moduleNames:
            self.assertIn(moduleName, MeetingPlace.loadedModules)

    def importModuleByName(self, moduleName):
        return __import__(moduleName, fromlist = [moduleName])
            
    def test_loads_modules_only_ones(self):
        moduleLoaded = '''if 1:
            import MeetingPlace
            MeetingPlace.loadedModules.append(__name__)
            '''
        moduleLoading = '''if 1:
            import moduleLoaded, MeetingPlace
            MeetingPlace.loadedModules.append(__name__)
            '''
        
        m1Name = self.addCache('moduleLoaded', moduleLoaded)
        m2Name = self.addCache('moduleLoading', moduleLoading)
        self.rep.addModuleDependency(self.importModuleByName(m1Name))
        self.rep.addModuleDependency(self.importModuleByName(m2Name))
        self.assertAllModulesLoaded([m1Name, m2Name])
        MeetingPlace.loadedModules = []
        self.dump_and_load()
        self.assertAllModulesLoaded([m1Name, m2Name])
        
        
    
if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

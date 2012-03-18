import unittest
import os


class FolderTestLoader(unittest.TestLoader):
    def __init__(self, folder):
        unittest.TestLoader.__init__(self)
        self.folder = folder
    
    def loadTestsFromModule(self, _):
        moduleNames = set()
        for fileName in os.listdir(self.folder):
            self.addModuleName(fileName, moduleNames)
        tests = []
        for moduleName in moduleNames:
            module = __import__(moduleName)
            tests.extend(unittest.TestLoader.loadTestsFromModule(self, module))
        return self.suiteClass(tests)
            

    def addModuleName(self, fileName, modules):
        if fileName.endswith('.py'):
            modules.add(fileName[:-3])
    


def main(folder = '.', *args, **kw):
    if len(args) < 5:
        kw.setdefault('testLoader', FolderTestLoader(folder))
    unittest.main(*args, **kw)
    
        
    
if __name__ == '__main__' :
    main(exit = False)
    import sys
    if not 'idlelib' in sys.modules:
        raw_input()

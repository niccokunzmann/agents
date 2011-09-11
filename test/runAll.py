
from test import *

if __name__ == '__main__':
    try:
        __file__
    except NameError:
        path = '.'
    else:
        path = os.path.split(__file__)[0]
    suite = unittest.TestSuite()
    caseset = dict()
    def addSuite(suite):
        for case in suite:
            if isinstance(case, unittest.TestSuite):
                addSuite(case)
                continue
            key = case.id()
            if key in caseset:
##                print 'in:', type(case).__name__
                pass
            else:
##                print 'new:', type(case).__name__
                caseset[key] = case

    for filename in os.listdir(path):
        if filename.startswith('test_'):
            filepath = os.path.join(path, filename)
            modname, ext = os.path.splitext(filename)
            if modname.endswith('dedicated'):
##                print 'skip:', modname
                continue
            if os.path.isfile(filepath) and ext.lower() in ('py', 'pyw'):
                mod = __import__(modname)
            else:
                try:
                    mod = __import__(modname)
                except ImportError:
                    ty, er, tb = sys.exc_info()
                    if tb.tb_next:
                        traceback.print_exception(ty, er, tb)
                    continue
            
            cases = unittest.defaultTestLoader.loadTestsFromModule(mod)
            addSuite(cases)
    l = caseset.values()
    l.append(suite)
    suite = unittest.TestSuite(l)
    unittest.TextTestRunner(verbosity=1).run(suite)

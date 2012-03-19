
from ReplicatingObject import R

PICKLEABLE___builtins__ = R(vars, R(__import__, '__builtin__'))
PICKLEABLE_FunctionType = R(type, R(eval, 'lambda:None'))

def packCode(code, globals = {}, add_builtins = True, use_same_globals = False, \
             check_syntax = True):
    '''return an object that executes code in globals when unpickled
if 'obj' exists in globals af ter the code execution
it is returned as result of the pickling operation
if 'obj' does not exist None is returned
use_same_globals
    if use_same_globals is True all codes sent through one pickle connection
    share the same globals
    by default the don't
'''
    if check_syntax:
        compile(code, '', 'exec')
    # copying locals is important
    # locals is transferred through pickle for all code identical
    # copying it prevents different code from beeing executed in same globals
    if not use_same_globals:
        globals = globals.copy() 
    if add_builtins:
        globals['__builtins__'] = PICKLEABLE___builtins__
    # get the compilation code
    # do not marshal or unmarshal code objects because the platforms may vary
    code = R(compile, code, __name__ + '.packCode()', 'exec')
    # the final object that can reduce, dump and load itself
    obj = R(R(getattr, tuple, '__getitem__'), (
            R(R(PICKLEABLE_FunctionType, code, globals)),
            R(R(getattr, type(globals), 'get'), globals, \
              'obj', None)
            ), -1)
    return obj

def packModule(module):
    '''return an object that becomes the module when unpickled
the module is local where the object is unpickled
the module is not copied to there nor must be the same module as
from the objects origin'''
    return R(__import__, module.__name__)

def packAttribute(object, attr):
    '''return an object that becomes objects attribute attr when unpickled'''
    return R(getattr, object, attr)

def _get_connection_back():
    import MeetingPlace
    import thread
    return MeetingPlace.connections_by_threadid.get(thread.get_ident(), None)

connection_back = R(_get_connection_back)

connection_back.__doc__ = '''
when unpickling this object turns into the last connection used by this thread.
those connections must be registered in MeetingPlace.connections_by_threadid.
'''

__all__ = ['packCode', 'packModule', 'packAttribute', 'connection_back']

#!/bin/env python
''' 



'''

import thread

_get_attr = getattr(object, '__getattr__', getattr(object, '__getattribute__'))

class _DefaultAttributes(object):
    '''
default.x = 3
-> set default value
default.x
-> is value set?
'''
    def __init__(self, obj):
        object.__setattr__(self, '__obj', obj)

    def __setattr__(self, name, value):
        _get_attr(self, '__obj').__dict__.setdefault(name, value)

    def __getattr__(self, name):
        return hasattr(_get_attr(self, '__obj'), name)

def _getDefault(cls, obj):
    class DefaultSubClass(cls, _DefaultAttributes):
        __init__ = _DefaultAttributes.__init__
        __new__ = _DefaultAttributes.__new__
    return DefaultSubClass(obj) 

class GlobalObject(object):
    '''
    this class creates objects that are unique by name
    it can be pickled
    it overrides the __new__ method - so be careful when overriding this
    use the .default attribute to set default values

    '''

    __objects = {} # name, type : obj
    __lock = thread.allocate_lock()

    def __new__(cls, name, *args, **kw):
        '''create a new GlobalObject and save it'''
        key = (cls, name)
        l = []
        with cls.__lock:
            obj = cls.__objects.get(key, l)
            if obj is l:
                obj = object.__new__(cls, *args, **kw)
                cls.__objects[key] = obj
                obj.__key = key
        return obj

    @classmethod
    def getObject(cls, key, default = None):
        '''get the object specified by key'''
        return cls.__objects.get(key, default)

    def __reduce__(self):
        '''makes this object picklable
no local state will be transferred via stream
override this if you need to create objects differently
on the other side of the stream'''
        return _loadGlobalObject, (self.__key,)

    def getName(self):
        '''get the name of the object that it was initialized with'''
        return self.__key[1]

    def getKey(self):
        '''get the key of the object'''
        return self.__key

    
    def default(self):
        return _getDefault(type(self), self)
    default = property(default, doc = '''handle default values
globalobject.default.attribute = value
    set the default value for attribute
b = globalobject.default.attribute2
if b is True:
    a value ist set for globalobject.attribute2
else:
    no value set for globalobject.attribute2''')


def _loadGlobalObject(key, args = (), kw = {}):
    '''pickle helper for global objects'''
    l = []
    obj = GlobalObject.getObject(key, l)
    if obj is l:
        return key[0](key[1], *args, **kw)
    return obj
    
    


#!/bin/env python
import thread



class GlobalObject(object):
    '''
    this class creates objects that are unique by name

    it can be pickled

    it overrides the __new__ method - so be careful when overridung this

    '''

    __objects = {}
    __lock = thread.allocate_lock()

    def __new__(cls, name, *args, **kw):
        with cls.__lock:
            l = []
            obj = cls.__objects.get(name, l)
            if obj is l:
                obj = object.__new__(cls, *args, **kw)
                cls.__objects[name] = obj
                obj.__name = name
        return obj

    @classmethod
    def loadObject(cls, name, *args):
        return cls.__objects.get(name, *args)

    def __reduce__(self):
        return _loadGlobalObject, (self.__name,)


def _loadGlobalObject(name):
    return GlobalObject.loadObject(name)


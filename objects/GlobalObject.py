#!/bin/env python
import thread



class GlobalObject(object):
    '''
    this class creates objects that are unique by name

    it can be pickled

    it overrides the __new__ method - so be careful when overridung this

    '''

    __objects = {} # name, type : obj
    __lock = thread.allocate_lock()

    def __new__(cls, name, *args, **kw):
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
    def loadObject(cls, key, *args):
        return cls.__objects.get(key, *args)

    def __reduce__(self):
        return _loadGlobalObject, (self.__key,)


def _loadGlobalObject(key):
    return GlobalObject.loadObject(key)


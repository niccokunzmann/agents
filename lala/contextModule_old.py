_defaultObj = object()

def contextWrapper(fct):
    def func(self, *args):
        thId = thread.get_ident()
        thIds = types.ModuleType.__getattribute__(self, 'threadIds')
        context = thIds.get(thId, thIds['default'])
        return fct(self, context, thIds, *args)
    return func

class ContextAwareModule(types.ModuleType):
    def __init__(self, *args):
        types.ModuleType.__setattr__(self, 'threadIds', \
                            {'default':{}})
        types.ModuleType.__init__(self, *args)


    @contextWrapper
    def __getattribute__(self, context, thIds, name):
        print id(context), name
        if name == '__dict__':
            return context
        obj = context.get(name, _defaultObj)
        if obj is _defaultObj:
            raise AttributeError('%s object has no attribute %s' % \
                                 (type(self).__name__, name))
        return obj

    @contextWrapper
    def __setattr__(self, context, thIds, name, value):
        if name == '__dict__':
            thIds[thread.get_ident()] = value
        else:
            context[name] = value

    @contextWrapper
    def __delattr__(self, context, thIds, name):
        del context[name]

    @classmethod
    def isContextAware(cls):
        return True

    @classmethod
    def makeContextAware(cls, fullname):
        new = cls(fullname)
        sys.modules.setdefault(fullname, new)
        mod = sys.modules[fullname]
        if hasattr(type(mod), 'isContextAware') and type(mod).isContextAware():
            type(mod).addContext(mod)
            return mod
        type(new).addContext(new)
        if new is not mod:
            type(new).setContext(new, 'default', mod.__dict__)
        return new

    @contextWrapper
    def addContext(self, context, thIds):
        thIds.setdefault(thread.get_ident(), {})

    @contextWrapper
    def setContext(self, context, thIds, contextName, newContext):
        thIds[contextName] = newContext


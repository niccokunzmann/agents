
import sys
import thread

import time as _time
import time


def yieldId():
    i = 0
    while 1:
        yield i
        i+= 1

_ids = yieldId()
def getId():
    while 1:
        try:
            return next(_ids) # todo: add error
        except ():
            pass

class _LogStream(object):
    def __init__(self, id, callBack):
        self.callBack = callBack
        self.id = id

    def flush(self):
        pass

    def write(self, string):
        self.callBack(self.id, string)

class BaseLog()


class StringLog(object):

    @staticmethod
    def getId(id = None):
        if id is None:
            return str(getId())
        return id

    def log(self, id, msg):
        raise NotImplementedError('needs to be overwritten')

    def logMethodCall(self, _, name, obj, args, kw, id = None):
        thread_id = thread.get_ident()
        time = _time.time()
        return self.logMethod('Method Call', locals())

    def logMethod(self, name, d):
        id = self.getId(d.pop('id', None))
        self.logMethodName(id, name)
        for key in d.keys():
            if key.startswith('_'):
                d.pop(key)
        self.log_dict(id, d)
        return id

    def log_dict(self, id, d):
        keys = d.keys()
        keys.sort()
        for key in keys:
            val = d[key]
            self.logKeyValue(id, key, val)

    def logKeyValue(self, id, key, value):
        self.log(id, key + ':')
        self.logValue(id, value)

    def logValue(self, id, value):
        self.log(id, '  = ' + repr(value))
        
    def logMethodName(self, id, name):
        self.log(id, '--> ' + name)

    def logMethodCallError(self, ty, er, tb, id = None):
        id = self.getId(id)
        f = _LogStream(id, self.logErrorLine)
        self.logMethodName(id, 'Method Call Error')
        traceback.print_exception(ty, er, tb, file= f)
        return id

    def logErrorLine(self, id, string):
        for line in string.split('\n'):
            self.log(id, 'exc:' + line)

    def logMethodCallValue(self, value, id = None):
        id = self.getId(id)
        self.logMethodName(id, 'Method Call Value')
        self.logTime(id)
        self.logValue(id, value)
        return id

    def logTime(self, id):
        self.log(id, 'time: %.3f' % time.time())

    def logCreateClass(self, cls, id = None):
        id = self.getId(id)
        self.logMethodName(id, 'Create Class Log')
        self.log_dict(id, dict(name = cls.__name__, module = cls.__module__))
        

class MethodCallLogger(object):
    def __init__(self, obj, methods, log):
        object.__setattr__(self, 'obj', obj)
        object.__setattr__(self, 'log', log)
        object.__setattr__(self, 'methods', methods)

    def __getattribute__(self, name):
        obj = object.__getattribute__(self, 'obj')
        methods = object.__getattribute__(self, 'methods')
        if name in methods:
            log = object.__getattribute__(self, 'log')
            func = getattr(obj, name)
            def logCall(*args, **kw):
                _id = log.logMethodCall(self, name, obj, args, kw)
                try:
                    value = func(*args, **kw)
                except:
                    ty, er, tb = sys.exc_info()
                    if tb.tb_next:
                        tb = tb.tb_next
                    log.logMethodCallError(ty, er, tb, id = _id)
                    raise ty, er, tb
                else:
                    log.logMethodCallValue(value, id = _id)
            logCall.__name__ = 'logCall_' + name
            return logCall
        return object.__getattribute__(obj, name)
        
class ListLog(StringLog):
    def __init__(self):
        self._log = []

    def log(self, *args):
        self._log.append(args)

    def getLog(self):
        return self._log

LOGBUFSIZE = 1024

class StreamLog(StringLog):
    '''create a log around a stream
the stream must own the write() and flush() methods
for multithreading purposes the write operations should be parallelisable
'''
    def __init__(self, stream, bufsize = None):
        self.stream = stream
        if bufsize is None:
            bufsize = LOGBUFSIZE
        self._bufsize = bufsize
        self._written = bufsize
        self._lock = thread.allocate_lock()

    def log(self, id, msg):
        self.write('\r\n%s:\t%s' % (id, msg))

    def write(self, s):
        '''write a string to the stream'''
        self.stream.write(s)
        self._written+= len(s)
        if self._written > self._bufsize and self._lock.acquire(False):
            try:
                self.stream.flush()
            finally:
                self._lock.release()

class FileLog(StreamLog):
    '''open a file for logging'''
    def __init__(self, filename, mode = 'w'):
        f = open(filename, mode)
        StreamLog.__init__(self, f)

loggedClasses = []

def logClass(log, methods):
    '''

@logClass(FileLog("MyStuff.log"), ['method'])
class MyStuff:
    def method(self, argument):
        ...
        return some_value

'''
    def logClassCall(cls):
        class MethodCallLogger_(cls, MethodCallLogger):
            pass
        class Log_(cls):
            def __new__(log_, *args, **kw):
                obj = cls.__new__(log_, *args, **kw)
                return MethodCallLogger_(obj, methods, log)
        MethodCallLogger_.__name__ += cls.__name__
        Log_.__name__ += cls.__name__
        loggedClasses.append((cls, methods))
        log.logCreateClass(Log_)
        return Log_
    return logClassCall

def logObject(log, obj, methods):
    '''logObject(log, obj, methods)
log all method calls to returned object
the returned object works as a proxy
'''
    return MethodCallLogger(obj, methods, log)

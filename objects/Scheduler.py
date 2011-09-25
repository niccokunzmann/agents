
import threading
import traceback
import thread
import heapq
import Queue
import time

_debugLock = thread.allocate_lock()
_globali = 0
_threadid = 0

def debugMethod(func):
    name = func.__name__
    def call(*args, **kw):
        global _globali
        try:
            s = '%s%r, %r' % (name, args, kw)
        except:
            s = '%s (...)' % name
        if 1:
            i = _globali
            _globali += 1
            print '%i-> %s' % (i, s)
        r = func(*args, **kw)
        s = '%i = %r' % (i, r)
        if 1:
            print s
        return r
    call.__name__ = name
    return call

##def debugMethod(func):
##    return func

class Scheduler(threading.Thread):

    debug = 1

    maxWaitingThreads = 1


    def __init__(self):
        threading.Thread.__init__(self)
        self._lock = thread.allocate_lock()
        self._newJobs = Queue.Queue()
        self.__jobs = [] # time, job
        self._doJobs = Queue.Queue()
        self.__stop = False
        self._lock = thread.allocate_lock()
        self.__running = 0
        self.__waiting = 0


    def stopped(self):
        return self.__stop


    def addJob(self, job, seconds):
        t = time.time() + seconds

        self._newJobs.put((job, t))


    def run(self):
        while not self.stopped():
            self.__addJobs(block = False)
            now = time.time()

            while self.__jobs:
                job, t = self.__getJob()
                if t < now:

                    self.__doJob(job)
                else:

                    self.__addJob(job, t)
                    time.sleep(0.001)
                    now = time.time()
            self.__addJobs(block = True) # last line in loop


    def __addJobs(self, block = True):
        while block or not self._newJobs.empty():
            newJob, time = self._newJobs.get()
            self.__addJob(newJob, time)
            block = False


    def __addJob(self, job, time):
        heapq.heappush(self.__jobs, (time, job))


    def __getJob(self):
        time, job = heapq.heappop(self.__jobs)
        return job, time
            

    def stop(self):
        self.__stop = True
        with self._lock:
            for i in xrange(self.__waiting + self.__running):
                self.__addJob(None, 0)
            self.addJob(None, 0)


    def __doJob(self, job):
        with self._lock:

            self._doJobs.put(job)
            if not self._maxThreadsReached():
                thread.start_new(self.runJob, ())


    def _maxThreadsReached(self):
        return self.__waiting >= self.maxWaitingThreads


    def runJob(self, *args, **kw):
        try:
            job = self.__waitJob()

            while job is not None and not self.stopped():

                self.__runJob(job)

                job = self.__waitJob()

        except:
            if self.debug >= 1:
                traceback.print_exc()
            

    def __waitJob(self):
        with self._lock:
            if self._maxThreadsReached():
                return None
            self.__waiting += 1

        try:
            return self._doJobs.get()
        finally:
            with self._lock:

                self.__waiting -= 1
    

    def __runJob(self, job):
        with self._lock:

            self.__running += 1
        try:
            job.run()
        except:
            if self.debug >= 1:
                traceback.print_exc()
        finally:
            with self._lock:

                self.__running -= 1
            
            

    






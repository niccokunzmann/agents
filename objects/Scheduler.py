
import threading
import thread
import heapq
import Queue
import time
    

def debugMethod(func):
    def call(*args, **kw):
        s = '%s%r, %s' % (func.__name__, args, kw)
        print s
        r = func(*args, **kw)
        print s, '=', r
        return r
    return call

class Scheduler(threading.Thread):

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
            print now
            while self.__jobs:
                job, t = self.__getJob()
                if t < now:
                    self.__doJob(job)
                else:
                    self.__addJob(job, t)
            self.__addJobs(block = True) # last line in loop

    def __addJobs(self, block = True):
        while block or not self._newJobs.empty():
            newJob, time = self._newJobs.get()
            self.__addJob(newJob, time)

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
            self._doJobs.push(job)
            if not self._maxThreadsReached():
                thread.start_new(self.runJob, ())

    def _maxThreadsReached(self):
        return self.__waiting >= self.maxWaitingThreads

    def runJob(self):
        job = self.__waitJob()
        while job is not None and not self.stopped():
            self.__runJob(job)
            job = self.__waitJob()
            
    def __waitJob(self):
            with self._lock:
                if self._maxThreadsReached():
                    return None
                self.__waiting += 1
            try:
                return self._doJobs.pop()
            finally:
                with self._lock:
                    self.__waiting -= 1
    
    def __runJob(self, job):
        with self._lock:
            self.__running += 1
        try:
            job.run()
        finally:
            with self._lock:
                self.__running -= 1
            
            

    






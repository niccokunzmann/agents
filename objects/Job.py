
from Scheduler import Scheduler

import sys
import traceback

defaultScheduler = Scheduler(10)
defaultScheduler.start()

_exitfunc = getattr(sys, 'exitfunc', lambda:None)
def exitfunc():
    _exitfunc()
    defaultScheduler.stop()

class Job(object):
    ''' a Job

use after(seconds) to have run() called after this time
override run to use the job class properly


'''

    def __init__(self, scheduler = defaultScheduler):
        self.setScheduler(scheduler)

    def run(self):
        '''this is the run method that should be overwritten'''
        raise NotImplementedError('this method must be overidden')

    def setScheduler(self, scheduler):
        '''set the scheduler'''
        self.__scheduler = scheduler

    def after(self, seconds):
        '''rerun this job after the specified time in seconds'''
        self.__scheduler.addJob(self, seconds)
        
class TimedJob(Job):
    '''
this job runs the do() method in an interval
'''
    debug = 1

    def __init__(self, interval, function = None):
        Job.__init__(self)
        self.interval = interval
        self.__stopped = False
        if function is not None:
            self.do = function
        self.next()

    def run(self):
        '''call do regularily'''
        if self.__stopped:
            return 
        try:
            self.do()
        except:
            if self.debug:
                traceback.print_exc()
        finally:
            self.next()

    def next(self):
        '''rerun after interval passed'''
        if not self.__stopped:
            self.after(self.interval)

    def stop(self):
        '''stop the timed job'''
        self.__stopped = True

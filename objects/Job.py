
from Scheduler import Scheduler

defaultScheduler = Scheduler(10)
defaultScheduler.start()

class Job(object):

    def __init__(self, scheduler = defaultScheduler):
        self.setScheduler(scheduler)

    def run(self):
        '''this is the run method that should be overwritten'''
        raise NotImplementedError('this method must be overidden')

    def setScheduler(self, scheduler):
        self.__scheduler = scheduler

    def after(self, seconds):
        '''rerun this job after the specified time in seconds'''
        self.__scheduler.addJob(self, seconds)
        

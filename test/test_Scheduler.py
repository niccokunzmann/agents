from test import *

from objects.Job import Job, Scheduler, defaultScheduler

class CountJob(Job):

    def __init__(self, count, timeout = 0.005, *args):
        Job.__init__(self, *args)
        self.count = count
        self.timeout = timeout
        
    def run(self):
##        print 'run', self.count
        self.count-= 1
        if self.count > 0:
            self.after(self.timeout)


class test_Job(unittest.TestCase):

    def test_count_1(self):
        c = CountJob(1)
        c.run()
        time.sleep(0.8)
        self.assertEqual(0, c.count)

    def test_count_3(self):
        c = CountJob(3)
        c.run()
        time.sleep(0.8)
        self.assertEqual(0, c.count)

class test_Scheduler(unittest.TestCase):

    def test_is_alive(self):
        self.assertTrue(defaultScheduler.isAlive(), 'the defaultScheduler must be alive')

    def test_addJob_1(self):
        job = CountJob(1)
        job.after(0)
        time.sleep(0.5)
        self.assertEqual(0, job.count)

    def test_addJob(self):
        job = CountJob(1)
        defaultScheduler.addJob(job, 0)
        time.sleep(0.5)
        self.assertEqual(0, job.count)

    def test_create_add(self):
        s = Scheduler()
        self.assertFalse(s.isAlive())
        self.assertFalse(s.stopped())
        self.assertTrue(s._newJobs.empty())
        j = CountJob(1, 0, s)
        s.addJob(j, 0.0)
        self.assertFalse(s._newJobs.empty())
        s.start()
        self.assertFalse(s.stopped())
        self.assertTrue(s.isAlive())
        time.sleep(0.5)
        self.assertTrue(s._newJobs.empty())

##del test_Scheduler

if __name__ == '__main__':
    unittest.main(exit = False)

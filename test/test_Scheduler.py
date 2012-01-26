from test import *

from objects.Job import Job, Scheduler, defaultScheduler

debug = True

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

    @unittest.skip('this is a performance test')
    def test_manyJobs(self):
        l=  []
        m = 200
        for i in range(1, m):
            j = CountJob(i, 0)
            j.after(0)
            l.append(j)
        s = m * m * j.timeout * 0.04 + 0.006* m
        print s
        time.sleep(s)
        for i, j in enumerate(l):
            self.assertEqual(0, j.count, '%i != 0 : %i' % (j.count,i))

    @unittest.skip('this is a performance test')
    def test_time(self):
        m = 2000000
        j = CountJob(m, 0)
        j.after(0)
        t = 10 # seconds
        time.sleep(t)
        c = m - j.count
        j.count = 0
        counts_per_sec = float(c) / t
        if debug:
            print 'counts per sec:', counts_per_sec

##debug = False

if __name__ == '__main__':
    unittest.main(exit = False)



from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw
from stream.IPPort import IPPort

debug = True

from stream.ClusterPart import ClusterPart, Group, ClusterIPPort
from stream.ClusterAgent import ClusterAgent
from stream.SimpleAgentPort import SimpleAgentPort


TIMEOUT_CLUSTER = 20
TIMEOUT_JOIN = 5
TIMEOUT_RECV = 1
TIMEOUT_SETUP = 1

class TestClusterPart(ClusterPart):

    portUpdateInterval = 1 # donnot change
    portBroadcastInterval = 1 # test_create_clusterPart

    def __init__(self, *args, **kw):
        ClusterPart.__init__(self, *args, **kw)
        self.connections = []

    def newConnection(self, connection):
##        print 'connection:', connection, connection.getAgent().getName(), \
##              connection.isLocal()
        self.connections.append(connection)
        ClusterPart.newConnection(self, connection)

class TestClusterAgent(ClusterAgent):
    pass

class SomeObject(object):
    pass

class test_build_cluster(unittest.TestCase):

    def setUp(self):
        time.sleep(TIMEOUT_SETUP)
        self.__cp = []

    def tearDown(self):
        for cp in self.__cp:
            cp.close()

    def newCP(self, *args):
        p = TestClusterPart(*args)
        self.__cp.append(p)
        return p

    def test_create_clusterPart(self):
        a = ClusterAgent('test_create_clusterPart', \
                         ['test_create_clusterPart'])
        self.p = self.newCP(a)
        self.assertEqual([Group('test_create_clusterPart')], self.p.getGroups())
        self.assertEqual('test_create_clusterPart', self.p.getName())
        v = 1
        for job in self.p.getJobs():
            self.assertEqual(v, job.interval, '%s == %s : for %s object' % (\
                v, job.interval, type(job.__name__)))

    @unittest.skip('todo')
    def test_join_one(self):
        a1 = ClusterAgent('test_join_one', ['test_join_one'])
        self.p = self.newCP(a1, [ClusterIPPort])
        p = launchClusterPart('test_build_cluster_dedicated.test_join_one', \
                          'test_join_one_1', ['test_join_one'])
        try:
            time.sleep(TIMEOUT_JOIN)
            g = Group('test_join_one')
            a2 = ClusterAgent('test_join_one_1')
            self.assertEqual([g], self.p.getGroups())
            self.assertNotEqual(0, len(self.p.connections))
            l = [con.getAgent().getName() for con in self.p.connections]
            self.assertIn('test_join_one', l, 'self broadcastet')
            self.assertIn('test_join_one_1', l, 'other broadcastet')
            self.assertIn(a1, g.getMembers())
            self.assertIn(a2, g.getMembers())
            self.assertTrue(a2.isConnected())
            a2.write('hallo?')
            a2.flush()
        finally:
            self.assertTrue(p.printOnFail())

##    @unittest.skip('try above')
    def test_join_n(self, n = 1, thread = False):
        # setup
        a1 = ClusterAgent('test_join_n', ['test_join_n'])
        self.p = self.newCP(a1, [ClusterIPPort])
        p_list = []
        for i in range(n):
            p = launchClusterPart('test_build_cluster_dedicated.test_join_n', \
                  'test_join_n_' + str(i), ['test_join_n'])
            p_list.append(p)
        time.sleep(TIMEOUT_JOIN + TIMEOUT_RECV)
        #test
        try:
            self.error = 0
            self.state = 'not ok'
            if thread:
                thread.start_new(self._join_n, (a1, n))
            else:
                self._join_n(a1, n)
            def check():
                1 / self.error
                raise TypeError()
            try:
                doTimeout(check, ZeroDivisionError, \
                          timeout = TIMEOUT_CLUSTER - TIMEOUT_JOIN)
            except TypeError:
                if self.error is None:
                    self.assertEquals('ok', self.state, 'reached the end')
                else:
                    raise self.error[0], self.error[1], self.error[2]
        finally:
            # teardown
            for p in p_list:
                self.assertTrue(p.printOnFail())

    def _join_n(self, a1, n):
        try:
            test_join_n = a1.getGroups()[0]
            self.assertEqual(n + 1, len(test_join_n.getMembers()), \
                             'all agents joined')
            for agent in test_join_n:
                if agent != a1:
                    self.state = 1
                    a1.update()
                    self.state = 2
                    greeting = a1.read(10)
                    self.state = 3
                    self.assertNotEqual([], greeting, 'greeting received')
                    self.assertNotEqual('', greeting, 'greeting received')
                    print 'greeting:', repr(greeting)
                    greeting = greeting[0]
                    self.state = 4
                    self.assertEqual('hello!', greeting.hello)
                    self.assertIn(greeting.agent, test_join_n)
                    self.state = 5
            self.state = 6
            if n >= 1:
                agent1 = ClusterAgent('test_join_n')
        except:
            self.error = sys.exc_info()
        else:
            self.state = 'ok'
            self.error = None
            


if __name__ == '__main__':
    unittest.main(exit = False)



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

class test_build_cluster(unittest.TestCase):

    def setUp(self):
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

##    @unittest.skip('todo')
    def test_join_one(self):
        a1 = ClusterAgent('test_join_one', ['test_join_one'])
        self.p = self.newCP(a1, [ClusterIPPort])
        p = launchClusterPart('test_build_cluster_dedicated.test_join_one', \
                          'test_join_one_1', ['test_join_one'])
        try:
            time.sleep(4)
            g = Group('test_join_one')
            a2 = ClusterAgent('test_join_one_1')
            self.assertEqual([g], self.p.getGroups())
            self.assertNotEqual(0, len(self.p.connections))
            l = [con.getAgent().getName() for con in self.p.connections]
            self.assertIn('test_join_one', l, 'self broadcastet')
            self.assertIn('test_join_one_1', l, 'other broadcastet')
            self.assertIn(a1, g.getMembers())
            self.assertIn(a2, g.getMembers())
            a2.write('hallo?')
            a2.flush()
        finally:
            self.assertTrue(p.printOnFail())
            


if __name__ == '__main__':
    unittest.main(exit = False)

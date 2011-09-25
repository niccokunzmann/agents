

from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw
from stream.IPPort import IPPort

debug = True

from stream.ClusterPart import ClusterPart, Group
from stream.ClusterAgent import ClusterAgent
from stream.IPPort import IPPort


class test_build_cluster(unittest.TestCase):

    def setUp(self):
        self.__cp = []

    def tearDown(self):
        for cp in self.__cp:
            cp.close()

    def newCP(self, *args):
        p = ClusterPart(*args)
        self.__cp.append(p)
        return p

    def test_create_clusterPart(self):
        self.p = self.newCP('test_create_clusterPart', \
                 ['test_create_clusterPart'])
        self.assertEqual([Group('test_create_clusterPart')], self.p.getGroups())
        self.assertEqual('test_create_clusterPart', self.p.getName())

    def test_join_one(self):
        a1 = ClusterAgent('test_join_one', ['test_join_one'])
        self.p = self.newCP(a1, [IPPort])
        p = launchClusterPart('test_build_cluster_dedicated.test_join_one', \
                          'test_join_one_1', ['test_join_one'])
        time.sleep(1)
        p.printOnFail()
        g = Group('test_join_one')
        a2 = ClusterAgent('test_join_one_1')
        self.assertEqual([g], self.p.getGroups())
        self.assertIn(a1, g.getMembers())
        self.assertIn(a2, g.getMembers())


if __name__ == '__main__':
    unittest.main(exit = False)

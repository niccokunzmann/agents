

from test import *
import socket
import select
import stream.CachingStringStream as css
import stream.StreamWrap as sw
from stream.IPPort import IPPort

debug = True

from stream.ClusterPart import ClusterPart, Group



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
        self.p = self.newCP('centrum', ['group1'])
        self.assertEqual([Group('group1')], self.p.getGroups())
        self.assertEqual('centrum', self.p.getName())

    def test_join_one(self):
        self.p = self.newCP('centrum', ['group1'])
        p = launchClusterPart('test_build_cluster_dedicated.test_join_cluster', \
                          'client1', ['group1'])
        time.sleep(1)
        p.printOnFail()
        self.assertEqual()


if __name__ == '__main__':
    unittest.main(exit = False)

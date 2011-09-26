

from test import *

from stream.ClusterPart import ClusterPart, ClusterAgent, ClusterIPPort
from test_build_cluster import TestClusterPart


class test_build_cluster_dedicated(unittest.TestCase):

    def setUp(self):
        self.__cp = []

    def tearDown(self):
        for cp in self.__cp:
            cp.close()

    def newCP(self, *args):
        p = TestClusterPart(agent, *args)
        self.__cp.append(p)
        return p

    def test_join_one(self):
        p = self.newCP([ClusterIPPort])
        time.sleep(10)



if __name__ == '__main__':
    name, groups = beClusterPart()
    agent = ClusterAgent(name, groups)
    l = []
    def test():
        try:
            unittest.main(exit = False, verbosity = 2)
        finally:
            l.append(1)
    thread.start_new(test, ())
    doTimeout(lambda :1/len(l), ZeroDivisionError, timeout = 30)
    print 'exiting'
    sys.exit(0)

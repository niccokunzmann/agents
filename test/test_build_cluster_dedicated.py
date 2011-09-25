

from test import *

from stream.ClusterPart import ClusterPart, ClusterAgent

class test_build_cluster_dedicated(unittest.TestCase):

    def setUp(self):
        self.__cp = []

    def tearDown(self):
        for cp in self.__cp:
            cp.close()

    def newCP(self):
        p = ClusterPart(agent)
        self.__cp.append(p)
        return p

    def test_join_one(self):
        p = self.newCP()
        time.sleep(0)



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
    doTimeout(lambda :1/len(l), ZeroDivisionError, timeout = 10)

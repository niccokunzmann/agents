

from test import *

from stream.ClusterPart import ClusterPart

class test_build_cluster_dedicated(unittest.TestCase):

    def setUp(self):
        self.__cp = []

    def tearDown(self):
        for cp in self.__cp:
            cp.close()

    def newCP(self):
        p = ClusterPart(name, groups)
        self.__cp.append(p)
        return p

    def test_join_cluster(self):
        p = self.newCP()
        time.sleep(3)



if __name__ == '__main__':
    name, groups = beClusterPart()
    l = []
    def test():
        try:
            unittest.main(exit = False, verbosity = 2)
        finally:
            l.append(1)
    thread.start_new(test, ())
    doTimeout(lambda :1/len(l), ZeroDivisionError, timeout = 10)

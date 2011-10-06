

from test import *

from stream.ClusterPart import ClusterPart, ClusterAgent, ClusterIPPort
from test_build_cluster import *

class HelloGreeting(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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

    def test_join_n(self):
        p = self.newCP([ClusterIPPort])
        a1 = ClusterAgent('test_join_n', ['test_join_n'])
        time.sleep(TIMEOUT_JOIN)
        self.assertTrue(a1.isConnected())
        a1.write(HelloGreeting(agent = agent, hello = 'hello!'))
        greetings = a1.read(1)
        time.sleep(TIMEOUT_RECV)
        



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
    doTimeout(lambda :1/len(l), ZeroDivisionError, timeout = TIMEOUT_CLUSTER)
    print 'exiting'
    sys.exit(0)

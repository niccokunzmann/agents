

from test import *


from stream.StringPort import StringPort, StringPortConnection

PORT = 1
HOST = 0

debug_time = False

class test_StringPort(unittest.TestCase):

    def setUp(self):
        self.pl = []
        self.p = self.newPort()
        self.__time = time.time()
        self.__ltime = self.__time
        self.__count = 0

    def time(self, s = ''):
        if not debug_time:
            return
        t = time.time()
        # code here
        print '%2i  %1.3f\t+ %1.3f' % (self.__count, \
                                       -self.__time + t, \
                                       -self.__ltime + t), s
        self.__count += 1
        # end code section
        t2 = time.time()
        dt = t2 - t
        self.__ltime = t2
        self.__time += dt

    def newPort(self):
        p = StringPort()
        self.pl.append(p)
        return p

    def tearDown(self):
        for p in self.pl:
            p.close()

    def test_broadcast(self):
        self.time('los')
        p1 = self.p
        self.time()
        p1.open()
        self.time()
        p2 = self.newPort()
        self.time()
        p2.open()
        self.time()
        p1.broadcast()
        self.time('x')
        p2.update()
        self.time()
        con = p2.read(1)
        self.time()
        self.assertNotEqual([], con, 'nothing received')
        self.time()
        con = con[0]
        self.time()
        return p1, p2, con

    def test_connect(self):
        p1, p2, c2 = self.test_broadcast()
        c2.connect()
        p1.update()
        c1 = p1.read()
        self.assertEqual(2, len(c1))
        for c1 in c1:
            if c1.getPeerAddr()[PORT] == 0:
                break
        else:
            self.fail('no connection received to other side')
        c1.connect()
##        print c1
##        print c1.stream
##        print c1.stream.stream
##        print c1.stream.stream.stream
        c1.write('na, was geht?\n')
        c1.write(':)')
        c1.flush()
        time.sleep(0.1)
        c2.update()
        s = c2.read()
        self.assertEqual('na, was geht?\n:)', s)
        
        

    
if __name__ == '__main__':
    unittest.main(exit = False)

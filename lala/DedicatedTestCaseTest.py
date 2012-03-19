import pickleHelp
import time
import distobj.objects.GlobalObject as GlobalObject

import DedicatedTestCase
import unittest

class TestMixin(object):
    def setUp(self):
        self.x = 1

    def test_mixin(self):
        self.assertEquals(self.x, 1)

class MixedInTestCase(TestMixin, unittest.TestCase):
    pass


WAIT_FOR_RESPONSE_TIME_SECONDS = 5
class DedicatedTestCaseTest(DedicatedTestCase.DedicatedTestCase):
    def test_nothing(self):
        pass

    def test_send_and_reply(self):
        obj = GlobalObject.GlobalObject(\
                                'DedicatedTestCaseTest.test_send_and_reply')
        obj.default.echo = 1
        echo = obj.echo
        code = pickleHelp.packCode('''if 1:
        import MeetingPlace
        import pickleHelp
        code = pickleHelp.packCode("""if 1:
            import RemoteTestCase
            obj = RemoteTestCase.GlobalObject.GlobalObject(\
                                'DedicatedTestCaseTest.test_send_and_reply')
            obj.echo += 1
            """)
            
        MeetingPlace.last_connection.write(code)
        MeetingPlace.last_connection.flush()
        
''')
        self.connection.write(code)
        self.connection.flush()
        time.sleep(WAIT_FOR_RESPONSE_TIME_SECONDS)
        self.assertEquals(obj.echo, echo + 1)

if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

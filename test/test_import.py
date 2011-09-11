from test import *


class test_import(unittest.TestCase):

    def test_import(self):
        import distobj

    def test_import_objects(self):
        import distobj.objects

    def test_import_stream(self):
        import distobj.stream


def test_module():
    unittest.main(exit = False)

if __name__ == '__main__':
    test_module()


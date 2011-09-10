from objects.GlobalObject import GlobalObject

class TestGlobalObject(GlobalObject):

    def __init__(self, name, *args):
        self.args = args

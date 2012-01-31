
import Agent

class OtherAgent(Agent.Agent):

    def __init__(self, *args):
        self.args = args

    def __getinitargs__(self):
        return self.args

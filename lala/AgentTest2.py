
import Agent

class OtherAgent(Agent.Agent):

    def __init__(self, *args):
        self.args = args

    def getInitArgs(self):
        return self.args

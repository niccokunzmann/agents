

import Agent
import AgentTest2

class Agent3(Agent.Agent):
    pass

class Agent4(AgentTest2.OtherAgent):
    pass

class StatefulAgent(Agent.Agent):
    def __init__(self, reply = None):
        self.reply = reply

    def __getstate__(self):
        return self.reply

    def __setstate__(self, reply):
        self.reply = reply







import unittest
import cPickle
import Agent
import AgentTest2
import sys
    

class AgentReduceTestCase(unittest.TestCase):

    def setUp(self):
        self.agent = Agent.Agent()
        self.red = self.agent.getReducableRepresentation()

    def test_can_reduce(self):
        self.assertNotEqual(self.agent.__reduce__(), None)


    def test_Agent_can_be_reduced(self):
        cPickle.dumps(self.agent)

    def test_agent_dump_load_to_agent(self):
        agent = cPickle.loads(cPickle.dumps(self.agent))
        self.assertEquals(type(agent).__name__, type(self.agent).__name__)

    def test_referencedModulesByAgentIncludesAgent(self):
        modules = self.red.getModulesReferencedByAgent()
        self.assertIn(Agent, modules)

class AgentTransitTest(unittest.TestCase):

    def setUp(self):
        while sys.meta_path:
            sys.meta_path.pop()
        import Agent
        import AgentTest2
        del sys.modules[Agent.__name__]
        del sys.modules[AgentTest2.__name__]

    def assertOtherClassAfterTransit(self, agent):
        agent2 = cPickle.loads(cPickle.dumps(agent))
        self.assertNotEqual(agent2, agent)
        self.assertEquals(type(agent2).__name__, type(agent).__name__)
        self.assertNotEqual(type(agent2), type(agent))
        
    def test_otherAgent_transits(self):
        agent = AgentTest2.OtherAgent()
        self.assertOtherClassAfterTransit(agent)

    def test_Agent_transits(self):
        agent = Agent.Agent()
        self.assertOtherClassAfterTransit(agent)

if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

        

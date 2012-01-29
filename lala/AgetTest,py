

import unittest
import cPickle
import Agent


class AgentReduceTestCase(unittest.TestCase):

    def setUp(self):
        self.agent = Agent.Agent()

    def test_can_reduce(self):
        self.assertNotEqual(self.agent.__reduce__(), None)


    def test_Agent_can_be_reduced(self):
        cPickle.dumps(self.agent)

    def test_agent_dump_load_to_agent(self):
        agent = cPickle.loads(cPickle.dumps(self.agent))
        self.assertEquals(type(agent).__name__, type(self.agent).__name__)

    def test_referencedModulesByAgentIncludesAgent(self):
        modules = self.agent.getModulesReferencedByAgent()
        self.assertIn(Agent, modules)


if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

        

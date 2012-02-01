

import unittest
import cPickle
import Agent
import AgentTest2
import sys
    

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
        modules = self.agent.requiredModules()
        import Agent
        self.assertIn(Agent, modules)

class AgentTransitBaseTest(unittest.TestCase):

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

class AgentTransitTest(AgentTransitBaseTest):
    def test_otherAgent_transits(self):
        agent = AgentTest2.OtherAgent()
        self.assertOtherClassAfterTransit(agent)

    def test_Agent_transits(self):
        agent = Agent.Agent()
        self.assertOtherClassAfterTransit(agent)

class AgentCreationTest(AgentTransitBaseTest):

    def setUp(self):
        super(type(self), self).setUp()
        self.agent = AgentTest2.OtherAgent()

    def test_agent_is_called_with_arguments(self):
        self.agent.args = (1,2,3)
        agent2 = cPickle.loads(cPickle.dumps(self.agent))
        self.assertEqual(agent2.args, self.agent.args)
        self.assertNotEqual(type(agent2), type(self.agent))

    def test_Agent_can_bePickled_several_times(self):
        self.agent.args = (1,2,3)
        agent2 = cPickle.loads(cPickle.dumps(self.agent))
        for i in range(100):
            agent2 = cPickle.loads(cPickle.dumps(agent2))
        self.assertEqual(agent2.args, self.agent.args)
        self.assertNotEqual(type(agent2), type(self.agent))

import Agent3

class PickleUnknownAgentsTest(AgentTransitBaseTest):

    def setUp(self):
        super(type(self), self).setUp()
    
    def test_Agent3(self):
        agent = Agent3.Agent3()
        self.assertTransits(agent)

    def test_Agent4(self):
        agent = Agent3.Agent4()
        self.assertTransits(agent)

    def assertTransits(self, agent):
        s = cPickle.dumps(agent)
        for module in agent.requiredModules():
            sys.modules.pop(module.__name__, None)
        agent2 = cPickle.loads(s)
        self.assertNotEqual(type(agent2), type(agent))
        self.assertEqual(type(agent2).__name__, type(agent).__name__)
        self.assertNotEqual(agent2.getModule(), sys.modules.get(agent2.__module__))

    def test_module_Agent3_in_transit_list(self):
        import Agent3
        agent = Agent3.Agent3()
        self.assertIn(Agent3, agent.requiredModules())

    def test_state_is_set(self):
        agent = Agent3.StatefulAgent('lalilu')
        s = cPickle.dumps(agent)
        agent2 = cPickle.loads(s)
        self.assertEquals(agent2.reply, 'lalilu')
        
        
        


if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)

        

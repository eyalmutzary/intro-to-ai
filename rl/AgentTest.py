# import unittest
# from valueIterationAgents import ValueIterationAgent
#
#
# class MockMDP:
#     def getStates(self):
#         return ['s1', 's2']
#
#     def getStartState(self):
#         return 's1'
#
#     def getPossibleActions(self, state):
#         if state == 's1':
#             return ['a1', 'a2']
#         elif state == 's2':
#             return ['a1']
#         return []
#
#     def getTransitionStatesAndProbs(self, state, action):
#         if state == 's1' and action == 'a1':
#             return [('s2', 1.0)]
#         elif state == 's1' and action == 'a2':
#             return [('s2', 0.5), ('s1', 0.5)]
#         elif state == 's2' and action == 'a1':
#             return [('s1', 1.0)]
#         return []
#
#     def getReward(self, state, action, nextState):
#         if state == 's1' and action == 'a1' and nextState == 's2':
#             return 10
#         elif state == 's1' and action == 'a2' and nextState == 's2':
#             return 5
#         elif state == 's2' and action == 'a1' and nextState == 's1':
#             return 7
#         return 0
#
#     def isTerminal(self, state):
#         # Assuming no terminal states for simplicity in this mock
#         return False
#
#
# class TestValueIterationAgent(unittest.TestCase):
#     def test_value_iteration(self):
#         mdp = MockMDP()
#         agent = ValueIterationAgent(mdp, discount=0.9, iterations=10)
#
#         # Test the values after running value iteration
#         self.assertAlmostEqual(agent.values['s1'], 12.25, places=2)
#         self.assertAlmostEqual(agent.values['s2'], 9.0, places=2)
#
#         # Test the policy
#         self.assertEqual(agent.policy['s1'], ['a1'])
#         self.assertEqual(agent.policy['s2'], ['a1'])
#
#
# if __name__ == '__main__':
#     unittest.main()

import unittest
from valueIterationAgents import ValueIterationAgent


class SimpleMDP:
    def __init__(self):
        self.states = ['A', 'B']
        self.terminal_states = {'B': 1.0}  # B is the terminal state with a reward of 1

    def getStates(self):
        return self.states

    def getStartState(self):
        return 'A'

    def getPossibleActions(self, state):
        if state == 'A':
            return ['move']
        elif state == 'B':
            return []
        return []

    def getTransitionStatesAndProbs(self, state, action):
        if state == 'A' and action == 'move':
            return [('B', 1.0)]
        return []

    def getReward(self, state, action, nextState):
        if state == 'A' and nextState == 'B':
            return 1.0
        return 0.0

    def isTerminal(self, state):
        return state == 'B'


class TestSimpleValueIteration(unittest.TestCase):
    def test_simple_value_iteration(self):
        mdp = SimpleMDP()
        agent = ValueIterationAgent(mdp, discount=0.9, iterations=10)

        # Check the value of state A after value iteration
        self.assertAlmostEqual(agent.values['A'], 0.9, places=2)
        self.assertAlmostEqual(agent.values['B'], 1.0, places=2)

        # Check that the policy for A is to move to B
        self.assertEqual(agent.policy['A'], 'move')


if __name__ == '__main__':
    unittest.main()

import numpy as np

import mdp, util
from collections import defaultdict
from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.policy = defaultdict(list)
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        for i in range(iterations):
            for state in mdp.getStates():
                v_opt = 0
                v_actions = mdp.getPossibleActions(state)
                for a in v_actions:
                    next_state_probs = mdp.getTransitionStatesAndProbs(state, a)
                    v_candidate = 0
                    for next_state, prob in next_state_probs:
                        v_candidate += prob * (mdp.getReward(state, a, next_state) + discount * self.values[next_state])
                    if v_candidate >= v_opt:
                        v_opt = v_candidate
                        self.policy[state].append(a)
                self.values[state] = v_opt

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getQValue(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        return np.random.choice(self.policy[state])


    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)

import numpy as np

import mdp, util
from collections import defaultdict


class ValueIterationAgent:
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
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.policy = {}

        for i in range(iterations):
            new_values = util.Counter()  # Store updated values for this iteration
            for state in mdp.getStates():
                if mdp.isTerminal(state):
                    continue  # Skip terminal states
                v_opt = float('-inf')
                best_actions = []

                for a in mdp.getPossibleActions(state):
                    v_candidate = 0
                    for next_state, prob in mdp.getTransitionStatesAndProbs(state, a):
                        v_candidate += prob * (
                                mdp.getReward(state, a, next_state) + self.discount * self.values[next_state])

                    if v_candidate > v_opt:
                        v_opt = v_candidate
                        best_actions = [a]  # Start a new list of best actions
                    elif v_candidate == v_opt:
                        best_actions.append(a)  # Add to the list of best actions

                new_values[state] = v_opt

                # Randomly select one of the best actions if there are ties
                self.policy[state] = np.random.choice(best_actions)

            self.values = new_values  # Update the values with the newly computed ones

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # def getQValue(self, state, action):
    #     """
    #       The q-value of the state action pair
    #       (after the indicated number of value iteration
    #       passes).  Note that value iteration does not
    #       necessarily create this quantity and you may have
    #       to derive it on the fly.
    #     """
    #     "*** YOUR CODE HERE ***"

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        return self.policy[state]

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)

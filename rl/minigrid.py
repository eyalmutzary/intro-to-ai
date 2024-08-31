import random
import sys
from typing import Type
from state import GameState
import mdp
import util

class minigrid(mdp.MarkovDecisionProcess):

    def __init__(self, initial_state: GameState):
        self.state = initial_state

    def getStates(self):

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        return self.state

    def getPossibleActions(self, state):
        return state.get_legal_actions()

    def getTransitionStatesAndProbs(self, state, action):

    def getReward(self, state, action, nextState):

    def isTerminal(self, state):


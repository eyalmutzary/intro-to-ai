import random
from agents import Agent

class RandomAgent(Agent):
    def get_action(self, game_state):
        """
        Returns a random action from the list of legal actions
        """
        return random.choice(game_state.get_legal_actions()).value

import abc
from game_state import GameState

class Agent:
    def __init__(self, evaluation_function=None, depth=2):
        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state: GameState):
        return


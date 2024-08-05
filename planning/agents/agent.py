import abc
from game_state import GameState

class Agent:
    def __init__(self, depth=2):
        self.evaluation_function = None
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state: GameState):
        return


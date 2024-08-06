import abc
from game_state import GameState
import random 

class Agent:
    def __init__(self, evaluation_function=None, depth=2):
        self.evaluation_function = eval_func_v1
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state: GameState):
        return


def eval_func_v1(game_state: GameState):
    return random.randint(0, 100)  # TODO: Implement a better evaluation function
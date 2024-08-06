import abc
from game_state import GameState, Direction, eval_func_v1
import random 

class Agent:
    def __init__(self, evaluation_function=None, depth=2):
        self.evaluation_function = eval_func_v1
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state: GameState):
        return



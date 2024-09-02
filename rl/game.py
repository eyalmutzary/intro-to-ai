# Description: This file contains the Game class which is responsible for running the game loop and training the agent.
from typing import List, Tuple

from minigrid.core.constants import IDX_TO_OBJECT
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper, \
    FlatObsWrapper
from RL_Agents import QLearningAgent
import maps


class GameQlearning:
    def __init__(self, env):
        self.env = SymbolicObsWrapper(env)
        self.agent = QLearningAgent(env=self.env)

    def run(self, episodes=1000):
        self.agent.learn(episodes)

    def close(self):
        self.env.close()


def _translate_observation(self, raw_observation) -> List[List[str]]:
    """
        Gets a raw image of the game, and translates it to a list of lists of strings where each string the name of the cell it contains.
    """
    translated_image = [[] for _ in range(len(raw_observation[0]))]
    for row in raw_observation:
        translated_row = [IDX_TO_OBJECT[abs(box.tolist()[2])] for box in row]
        for i, val in enumerate(translated_row):  # for rotation
            translated_image[i].append(val)
    return translated_image


if __name__ == "__main__":
    # Replace with your specific MiniGrid environment
    game = GameQlearning(env=maps.MazeEnv(render_mode="human"))
    game.run(episodes=1000)
    game.close()

# Description: This file contains the Game class which is responsible for running the game loop and training the agent.
from typing import List, Tuple

from minigrid.core.constants import IDX_TO_OBJECT
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
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
        for i, val in enumerate(translated_row): # for rotation
            translated_image[i].append(val)
    return translated_image
# class GamePPO:
#     def __init__(self, env_name="MiniGrid-ObstructedMaze-1Dl-v0", n_envs=4, total_timesteps=100000):
#         self.agent = PPOAgent(env_name=env_name, n_envs=n_envs, total_timesteps=total_timesteps)
#
#     def run(self, train=True, model_path=None, n_episodes=5):
#         """Run the game with the PPO agent."""
#         if train:
#             self.agent.train()
#         else:
#             self.agent.load_and_run(model_path=model_path, n_episodes=n_episodes)
#
#     def close(self):
#         """Close the game and the environment."""
#         self.agent.close()


# if __name__ == "__main__":
    # game = GamePPO(env_name="MiniGrid-ObstructedMaze-1Dl-v0", n_envs=4, total_timesteps=100000)
    # game.run(train=True)  # To train the agent
    # # game.run(train=False, model_path="ppo_MiniGrid-ObstructedMaze-1Dl-v0", n_episodes=5)  # To load and run the agent
    # game.close()

if __name__ == "__main__":
    # Replace with your specific MiniGrid environment
    game = GameQlearning(env=maps.DoorsV1Env(render_mode="human"))
    game.run(episodes=1000)
    game.close()
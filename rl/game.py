# Description: This file contains the Game class which is responsible for running the game loop and training the agent.
from typing import List, Tuple
import gymnasium as gym

from minigrid.core.constants import IDX_TO_OBJECT
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper, ActionBonus, \
    PositionBonus, ViewSizeWrapper
from RL_Agents import QLearningAgent
import maps
import CustomMinigridWrapper
import constants

class GameQlearning:
    def __init__(self, env, policy_file=None):
        self.env = CustomMinigridWrapper.CustomMinigridWrapper(env)
        # self.env = PositionBonus(self.env) # Add PositionBonus wrapper
        # self.env = ViewSizeWrapper(self.env, agent_view_size=3) # Get pixel observations
        self.agent = QLearningAgent(env=self.env, policy_file=policy_file)

    def run(self, episodes=50):
        self.agent.train(episodes)

    def play(self, episodes=10):
        for _ in range(episodes):
            observation, info = self.env.reset()
            state = self.agent.get_state_from_obs(observation)
            done = False
            while not done:
                action = self.agent.act(state)
                observation, reward, terminated, truncated, info = self.env.step(action)
                state = state.generate_successor(constants.Action(action))
                done = terminated or truncated

    def close(self):
        self.env.close()


if __name__ == "__main__":
    # Replace with your specific MiniGrid environment
    # game = GameQlearning(gym.make('MiniGrid-Empty-5x5-v0', render_mode="human"), policy_file="qTable/policy.csv")
    # game = GameQlearning(gym.make('MiniGrid-Empty-5x5-v0', render_mode="human"))
    # game = GameQlearning(env=maps.MazeEnv(render_mode="human", agent_view_size=3), policy_file="qTable/policy.csv")
    # game = GameQlearning(env=maps.MazeEnv(render_mode="human"))
    # game = GameQlearning(env=maps.LavaMazeEnv(render_mode="human"), policy_file="qTable/policy.csv")
    game = GameQlearning(env=maps.DoorsV1Env(render_mode="human", agent_view_size=3))
    # game = GameQlearning(env=maps.LavaMazeEnv(render_mode="human"))
    game.run(episodes=2500)
    # game.play(10)
    game.close()

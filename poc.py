# https://minigrid.farama.org/environments/minigrid/DistShiftEnv/

import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from minigrid.core.constants import COLOR_TO_IDX, OBJECT_TO_IDX, STATE_TO_IDX

    # """
    # 0 - Turn left
    # 1 - Turn right
    # 2 - Move forward 
    # 3 - Pickup an object
    # """
env = gym.make("MiniGrid-DistShift2-v0", render_mode="human")
env = ViewSizeWrapper(env, agent_view_size=3) # Get pixel observations
# env = SymbolicObsWrapper(env)

observation, info = env.reset()
for _ in range(1000):
    # action = env.action_space.sample()
    action=0
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()
        
env.close()

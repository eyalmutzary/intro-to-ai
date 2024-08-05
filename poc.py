# https://minigrid.farama.org/environments/minigrid/DistShiftEnv/

import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from minigrid.core.constants import COLOR_TO_IDX, OBJECT_TO_IDX, STATE_TO_IDX, IDX_TO_OBJECT

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

    # """
    # 0 - Turn left
    # 1 - Turn right
    # 2 - Move forward 
    # 3 - Pickup an object
    # """
env = gym.make("MiniGrid-DistShift2-v0", render_mode="human")
env = ViewSizeWrapper(env, agent_view_size=3) # Get pixel observations
# env = SymbolicObsWrapper(env)

def observation_reader(image):
    result = []
    for row in image:
        result.append([])
        for box in row:
            result[-1].insert(0, IDX_TO_OBJECT[box.tolist()[0]])
    print(result)

def get_player_location_in_image(image):
    return (len(image)//2, 0)

observation, info = env.reset()
for _ in range(1000):
    # action = env.action_space.sample()
    action=3
    observation, reward, terminated, truncated, info = env.step(action)
    observation_reader(observation['image'])
    get_player_location_in_image(observation['image'])
    # print(observation)
    if terminated or truncated:
        observation, info = env.reset()
        
env.close()

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
# env = ViewSizeWrapper(env, agent_view_size=3) # Get pixel observations
env = SymbolicObsWrapper(env)

# def observation_reader(image):
#     result = []
#     for row in image:
#         result.append([])
#         for box in row:
#             result[-1].insert(0, IDX_TO_OBJECT[box.tolist()[0]])
#     print(result)

def rotate_matrix_90_degrees(matrix):
    # Transpose the matrix
    transposed_matrix = [list(row) for row in zip(*matrix)]
    # Reverse each row
    rotated_matrix = [row[::-1] for row in transposed_matrix]
    return rotated_matrix

def observation_reader(image):
    result = [[] for _ in range(len(image[0]))]
    for row in image:
        translated_row = [IDX_TO_OBJECT[abs(box.tolist()[2])] for box in row]
        for i, val in enumerate(translated_row): # for rotation
            result[i].append(val)
    
    # for printing:
    printed_string = ""
    for row in result:
        printed_string += " ".join(row) + "\n"
    
    print(printed_string)
    return result

def get_player_location_in_image(image):
    return (len(image)//2, 0)

observation, info = env.reset()
for _ in range(1000):
    action=3
    observation, reward, terminated, truncated, info = env.step(action)
    print(observation)
    # observation_reader(observation['image'])
    # get_player_location_in_image(observation['image'])
    if terminated or truncated:
        observation, info = env.reset()
        
env.close()

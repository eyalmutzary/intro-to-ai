from collections import deque
from time import sleep
from typing import List, Tuple
import gymnasium as gym

from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from state import GameState 
from minigrid.core.constants import IDX_TO_OBJECT
from minigrid_problem import MinigridProblem
from search_algorithms import depth_first_search, breadth_first_search, uniform_cost_search, a_star_search, improved_heuristic
from constants import Action, GAME_MAPS
from maps.maze import MazeEnv
from maps.door_simple import DoorSimple

class Game:
    def __init__(self):
        # self.env = gym.make("MiniGrid-ObstructedMaze-Full-v0", render_mode="human")
        self.env = DoorSimple(render_mode="human")
        self.env = SymbolicObsWrapper(self.env)

        
    def run(self):
        observation, info = self.env.reset()
        done = False
        last_target = None
        # path = depth_first_search(problem)
        # path = breadth_first_search(problem)
        # path = uniform_cost_search(problem)
        while not done:
            game_map = self._translate_observation(observation['image'])
            state = GameState(game_map, observation['direction'], is_picked_key=last_target=='key')
            problem = MinigridProblem(state)
            
            path = a_star_search(problem, improved_heuristic)
            moves = self._convert_search_path_to_moves(path, state.goal_name)
                        
            i = 0
            while i < len(moves):
                observation, reward, terminated, truncated, info = self.env.step(moves[i])
                done = terminated or truncated
                i+= 1
            last_target = state.goal_name
        self.close()
    
    def reset(self):
        return self.env.reset()
    
    def step(self, action):
        return self.env.step(action)
    
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
    
    def _convert_search_path_to_moves(self, path: List[Action], goal_name: str) -> List[int]:
        moves = []
        for action in path:
            moves.append(action.value)
            if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
                moves.append(Action.MOVE_FORWARD.value)
                
        if goal_name == 'door':
            moves.append(Action.MOVE_FORWARD.value) # enter the door after openning it

        return moves
    
if __name__ == "__main__":
    game = Game()
    game.run()
    game.close()
    

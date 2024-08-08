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
        # self.env = gym.make(GAME_MAPS[4], render_mode="human")
        self.env = DoorSimple(render_mode="human")
        self.env = SymbolicObsWrapper(self.env)

        
    def run(self):
        observation, info = self.env.reset()
        done = False
        game_map = self._translate_observation(observation['image'])
        state = GameState(game_map, self._find_next_target(game_map)[1], observation['direction'])
        problem = MinigridProblem(state)
        # print(state)
        # path = depth_first_search(problem)
        # path = breadth_first_search(problem)
        # path = uniform_cost_search(problem)
        path = a_star_search(problem, improved_heuristic)
        
        moves = []
        for action in path:
            moves.append(action)
            if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
                moves.append(Action.MOVE_FORWARD)
        
        # moves = [2,2,1,2,2,2,2,3,2,0,2,5,2,2,2,2,1,2]
        
        i = 0
        while not done and i < len(moves):
            game_map = self._translate_observation(observation['image'])
            state = GameState(game_map, self._find_next_target(game_map)[1],observation['direction'])
            observation, reward, terminated, truncated, info = self.env.step(moves[i].value)
            done = terminated or truncated
            i+= 1
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
    

    def _find_next_target(self, observation: List[List[str]]) -> tuple:
        # find the location of 'agent'
        for i, row in enumerate(observation):
            for j, cell in enumerate(row):
                if cell == 'agent':
                    start = (i, j)
                    break
        if start is None:
            raise ValueError("Player location not found in game map")
        
        rows, cols = len(observation), len(observation[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        queue = deque([start])
        visited = set()
        visited.add(start)
        
        found_goal = None
        found_key = None
        found_door = None
        
        while queue:
            r, c = queue.popleft()
            
            # Check and mark if we found any of the targets
            if observation[r][c] == 'goal':
                found_goal = (r, c)
            elif observation[r][c] == 'key':
                found_key = (r, c)
            elif observation[r][c] == 'door':
                found_door = (r, c)
            
            # Explore neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check if the neighbor is within bounds and is not a wall or visited
                if 0 <= nr < rows and 0 <= nc < cols and observation[nr][nc] not in ['wall', 'lava'] and (nr, nc) not in visited:
                    if observation[nr][nc] == 'door': # a door could be a target, but it should not be passable
                        found_door = (nr, nc)
                        continue
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        # Return based on priority
        if found_goal:
            return ('goal', found_goal)
        elif found_key:
            return ('key', found_key)
        elif found_door:
            return ('door', found_door)
        else:
            return None
    
    
    
if __name__ == "__main__":
    game = Game()
    game.run()
    game.close()
    

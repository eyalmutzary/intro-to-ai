from typing import List, Tuple
import gymnasium as gym

from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from state import GameState 
from minigrid.core.constants import IDX_TO_OBJECT
from minigrid_problem import MinigridProblem
from search_algorithms import a_star_search, improved_heuristic
from constants import Action, GAME_MAPS
import maps

class Game:
    def __init__(self, env):
        self.env = env
        self.env = SymbolicObsWrapper(self.env)

        
    def run(self):
        observation, info = self.env.reset()
        done = False
        last_target = None
        
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
        for i, action in enumerate(path):
            moves.append(action.value)
            if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
                moves.append(Action.MOVE_FORWARD.value)
            if action == Action.PICKUP and i < len(path) - 1: # edge case where doing pickup when the goal is not a key
                moves.append(Action.MOVE_FORWARD.value)
                
        if goal_name == 'key':
            moves.append(Action.PICKUP.value)
        
        if goal_name == 'door':
            moves.append(Action.MOVE_FORWARD.value) # enter the door after openning it
            moves.append(Action.MOVE_FORWARD.value) # drop the used key next to the door
            moves.append(Action.TURN_RIGHT.value)
            moves.append(Action.DROP.value)

        return moves
    
if __name__ == "__main__":
    # env = gym.make("MiniGrid-ObstructedMaze-Full-v0", render_mode="human")
    game = Game(env=maps.DoorsV3Env(render_mode="human"))
    game.run()
    game.close()
    

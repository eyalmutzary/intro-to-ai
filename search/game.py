import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from state import GameState 
from time import sleep
from typing import List
from minigrid.core.constants import IDX_TO_OBJECT
from minigrid_problem import MinigridProblem
from search_algorithms import depth_first_search, breadth_first_search, uniform_cost_search, a_star_search, improved_heuristic
from state import Action

Enviroments = [
    'MiniGrid-Empty-8x8-v0',
    'MiniGrid-Empty-16x16-v0',
    'MiniGrid-Empty-Random-6x6-v0',
    'MiniGrid-LavaGapS7-v0',
    'MiniGrid-DistShift2-v0',
]

class Game:
    def __init__(self):
        self.env = gym.make(Enviroments[4], render_mode="human")
        self.env = SymbolicObsWrapper(self.env)

        
    def run(self):
        observation, info = self.env.reset()
        done = False
        game_map = self._translate_observation(observation['image'])
        state = GameState(game_map, self._find_goal_location(game_map), observation['direction'])
        problem = MinigridProblem(state)
        
        # path = depth_first_search(problem)
        # path = breadth_first_search(problem)
        # path = uniform_cost_search(problem)
        path = a_star_search(problem, improved_heuristic)
        
        moves = []
        for action in path:
            moves.append(action)
            if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
                moves.append(Action.MOVE_FORWARD)
        print(len(moves))
        
        i = 0
        while not done and i < len(moves):
            state = GameState(self._translate_observation(observation['image']), observation['direction'])
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
    
    def _find_goal_location(self, observation: List[List[str]]) -> tuple:
        for i, row in enumerate(observation):
            for j, cell in enumerate(row):
                if cell == 'goal':
                    return (i, j)
        return None
    
    
    
if __name__ == "__main__":
    game = Game()
    game.run()
    game.close()
    

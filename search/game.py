import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from state import GameState 
from time import sleep
from typing import List
from minigrid.core.constants import IDX_TO_OBJECT

Enviroments = [
    'MiniGrid-Empty-16x16-v0',
    'MiniGrid-Empty-Random-6x6-v0',
    'MiniGrid-LavaGapS7-v0',
    'MiniGrid-DistShift2-v0',
]

class Game:
    def __init__(self, view_size=3):
        self.env = gym.make(Enviroments[3], render_mode="human")
        self.env = SymbolicObsWrapper(self.env)

        
    def run(self):
        observation, info = self.env.reset()
        done = False
        while not done:
            state = GameState(self._translate_observation(observation['image']), observation['direction'])
            # sleep(1)
            observation, reward, terminated, truncated, info = self.env.step(0)
            done = terminated or truncated
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
    
    
    
if __name__ == "__main__":
    # game = Game()
    # game.init(RandomAgent())
    # game = Game(AlphaBetaAgent(depth=2), view_size=13)
    game = Game(view_size=13)
    game.run()
    game.close()
    

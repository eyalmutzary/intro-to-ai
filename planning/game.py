import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from game_state import GameState 
from agents import RandomAgent, Agent, AlphaBetaAgent, PlanningAgent
from time import sleep

Enviroments = [
    'MiniGrid-Empty-16x16-v0',
    'MiniGrid-Empty-Random-6x6-v0',
    'MiniGrid-LavaGapS7-v0',
    'MiniGrid-DistShift2-v0',
]

class Game:
    def __init__(self, agent, view_size=3):
        self.env = gym.make(Enviroments[1], render_mode="human")
        self.env = ViewSizeWrapper(self.env, view_size)
        self.agent: Agent = agent
        
    def run(self):
        observation, info = self.env.reset()
        done = False
        while not done:
            state = GameState(observation['image'])
            action = self.agent.get_action(state)
            print("#### Action decided: ", action)
            # sleep(1)
            observation, reward, terminated, truncated, info = self.env.step(action)
            done = terminated or truncated
        self.close()
    
    def reset(self):
        return self.env.reset()
    
    def step(self, action):
        return self.env.step(action)
    
    def close(self):
        self.env.close()
    
    
    
if __name__ == "__main__":
    # game = Game()
    # game.init(RandomAgent())
    # game = Game(AlphaBetaAgent(depth=2), view_size=13)
    game = Game(PlanningAgent(depth=3), view_size=13)
    game.run()
    game.close()
    

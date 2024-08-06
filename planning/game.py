import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper, ViewSizeWrapper, SymbolicObsWrapper
from game_state import GameState 
from agents import RandomAgent, Agent, AlphaBetaAgent

class Game:
    def init(self, agent, view_size=3):
        self.env = gym.make("MiniGrid-DistShift2-v0", render_mode="human")
        self.env = ViewSizeWrapper(self.env, view_size)
        self.agent: Agent = agent
        
    def run(self):
        observation, info = self.env.reset()
        done = False
        while not done:
            state = GameState(observation['image'])
            action = self.agent.get_action(state)
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
    game = Game()
    # game.init(RandomAgent())
    game.init(AlphaBetaAgent())
    game.run()
    game.close()
    

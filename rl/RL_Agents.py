import numpy as np
from collections import defaultdict
import gymnasium as gym
import util


class QLearningAgent:
    def __init__(self, env, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, alpha=0.0005):
        self.env = env
        # self.q_value_function = {}
        # self.visited_actions = {}
        self.action_space_size = self.env.action_space.n
        self.visited_states = set()
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.alpha = alpha
        self.q_value_function = defaultdict(lambda: 0, {})
        self.visited_actions = defaultdict(lambda: [False] * self.action_space_size, {})

    def act(self, state):
        if np.random.rand() < self.epsilon:
            return self.env.action_space.sample()
        else:
            action, value = util.get_max_action(state, self.q_value_function, self.env)
            if value == 0:
                if False in self.visited_actions[state]:
                    action = self.visited_actions[state].index(False)
                else:
                    action = self.env.action_space.sample()
        return action

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_q_table(self, state, action, reward, next_state):
        q_value = self.q_value_function[state][action]
        next_q_value = np.max(self.q_value_function[next_state])
        self.q_value_function[state][action] = q_value + self.alpha * (reward + self.gamma * next_q_value - q_value)

    def learn(self, episodes):
        for e in range(episodes):
            observation, info = self.env.reset()
            state = str(self.env)
            done = False
            while not done:
                self.visited_states.add(state)
                action, value = self.act(state)
                next_observation, reward, terminated, truncated, _ = self.env.step(action)
                next_state = self.translate_state(next_observation)
                done = terminated or truncated
                self.update_q_table(state, action, reward, next_state)
                state = next_state
            self.decay_epsilon()
    #
    # def translate_state(self, observation):
    #     """Translate the observation to a state tuple that can be used as a key in the Q-table."""
    #     agent_pos = tuple(observation['image'].flatten())  # Flatten the image to create a simple state representation
    #     direction = observation['direction']
    #     return agent_pos, direction

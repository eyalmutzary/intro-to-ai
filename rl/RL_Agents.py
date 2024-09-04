import csv
import time
import numpy as np
from collections import defaultdict
import gymnasium as gym
import util
import pandas as pd
from enum import Enum
from typing import List, Tuple
from minigrid.core.constants import IDX_TO_OBJECT


class PlayerMode(Enum):
    TRAIN = 1
    PLAY = 2


class QLearningAgent:
    def __init__(self, env, gamma=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.99, alpha=0.05, policy_file=None):
        self.env = env
        self.visited_states = set()
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.alpha = alpha
        self.q_value_function = defaultdict(lambda: 0, {})
        self.visited_actions = defaultdict(lambda: [False] * self.env.action_space.n, {})
        self.mode = PlayerMode.TRAIN
        self.policy = None
        if policy_file:
            self.load_policy(policy_file)

    def load_policy(self, policy_file):
        """Load policy from a CSV file."""
        df = pd.read_csv(policy_file, index_col=0)
        # Convert DataFrame to Series and then to dictionary
        policy_dict = df.squeeze().to_dict()
        self.policy = defaultdict(lambda: -1, policy_dict)
        self.mode = PlayerMode.PLAY

    def act(self, state):
        if self.mode == PlayerMode.TRAIN:
            if np.random.rand() < self.epsilon:
                action = self.env.action_space.sample()
            else:
                action, value = util.get_max_action(state, self.q_value_function, self.env)
        else:
            action = self.policy[state]
            if action == -1:
                action = self.env.action_space.sample()
        return action

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_q_table(self, state, action, reward, next_state):
        next_action, next_q_value = util.get_max_action(next_state, self.q_value_function, self.env)
        max_q_value_target = reward + self.gamma * next_q_value
        self.q_value_function[(state, action)] = (1 - self.alpha) * \
                                                 self.q_value_function[
                                                     (state, action)] + self.alpha * max_q_value_target

    def train(self, episodes, model_dir='qTable'):
        episodes_length = []

        for e in range(episodes):
            print(f"iter: {e}")
            current_length = 0
            observation, info = self.env.reset()
            # state = str(self.env)
            state = self.translate_state(observation)
            done = False
            while not done:
                self.visited_states.add(state)
                action = self.act(state)
                self.visited_actions[state][action] = True

                next_observation, reward, terminated, truncated, _ = self.env.step(action)
                current_length += 1
                if terminated:
                    print (f"reached the goal with {current_length} steps at iter: {e}")
                # next_state = str(self.env)
                next_state = self.translate_state(next_observation)
                done = terminated or truncated
                self.update_q_table(state, action, reward, next_state)
                state = next_state
            self.decay_epsilon()
            episodes_length.append(current_length)
        print("[Statistics]: Avg_length {0}".format(sum(episodes_length) / len(episodes_length)))

        self.save_train_results(model_dir)

    def save_train_results(self, model_dir):
        file = open(model_dir + '/q_value.csv', "w")
        fieldnames = ['state', 'action', 'value']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for key, value in self.q_value_function.items():
            state, action = key
            writer.writerow({'state': state, 'action': action, 'value': value})
        file.close()

        file = open(model_dir + '/policy.csv', "w")
        fieldnames = ['state', 'action']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for state in self.visited_states:
            action, value = util.get_max_action(state, self.q_value_function, self.env)
            if value == 0:
                action = -1
            writer.writerow({'state': state, 'action': action})
        file.close()

    def translate_state(self, observation):
        """Translate the observation to a state tuple that can be used as a key in the Q-table."""
        agent_pos = tuple(observation['image'].flatten())  # Flatten the image to create a simple state representation
        direction = observation['direction']
        return agent_pos, direction
    #
    # def translate_state(self, observation):
    #     """Translate the observation to a state tuple that can be used as a key in the Q-table."""
    #     agent_pos = observation['image'].flatten()
    #     agent_pos = tuple(int(x) for x in agent_pos)  # Flatten the image to create a simple state representation
    #     direction = observation['direction']
    #     return agent_pos, direction

    # def _translate_observation(self, raw_observation) -> List[List[str]]:
    #     """
    #         Gets a raw image of the game, and translates it to a list of lists of strings where each string the name of the cell it contains.
    #     """
    #     translated_image = [[] for _ in range(len(raw_observation[0]))]
    #     for row in raw_observation:
    #         translated_row = [IDX_TO_OBJECT[abs(box.tolist()[2])] for box in row]
    #         for i, val in enumerate(translated_row):  # for rotation
    #             translated_image[i].append(val)
    #     return translated_image

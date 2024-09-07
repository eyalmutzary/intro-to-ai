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
from state import GameState
import constants

class PlayerMode(Enum):
    TRAIN = 1
    PLAY = 2


class QLearningAgent:
    def __init__(self, env, gamma=0.8, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, alpha=0.15,
                 policy_file=None):
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
        legal_actions = state.get_legal_actions()
        if self.mode == PlayerMode.TRAIN:
            if np.random.rand() < self.epsilon:
                action = np.random.choice(legal_actions)
            else:
                action, value = util.get_max_action(state, self.q_value_function)
                if value == 0 or action is None:
                    unvisited_actions = [a for a in legal_actions if not self.visited_actions[state][a.value]]
                    if unvisited_actions:
                        action = unvisited_actions[0]
                    else:
                        action = np.random.choice(legal_actions)
        else:
            action = self.policy[str(state)]
            if action != -1:
                return action
            action = np.random.choice(legal_actions)
        return action.value

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_q_table(self, state, action, reward, next_state):
        if next_state.is_goal_state():  # Assuming next_state has an `is_terminal()` method
            max_q_value_target = reward  # No future reward because it's the goal state
        else:
            next_action, next_q_value = util.get_max_action(next_state, self.q_value_function)
            max_q_value_target = reward + self.gamma * next_q_value

        # Q-value update
        self.q_value_function[(state, action)] = (1 - self.alpha) * \
                                                 self.q_value_function[(state, action)] + \
                                                 self.alpha * max_q_value_target

    def train(self, episodes, model_dir='qTable'):
        episodes_length = []

        for e in range(episodes):
            print(f"iter: {e}")
            current_length = 0
            observation, info = self.env.reset()
            game_state = self.get_state_from_obs(observation)
            # state = self.translate_state(observation)
            done = False
            while not done:
                self.visited_states.add(game_state)
                action = self.act(game_state)
                self.visited_actions[game_state][action] = True

                next_observation, reward, terminated, truncated, _ = self.env.step(action)
                current_length += 1
                if terminated:
                    # if game_state.is_goal_state():
                    #     reward *= 10
                    # else:
                    #     reward = -10
                    print(f"reached the goal with {current_length} steps at iter: {e}, and reward: {reward}")
                if truncated:
                    print(f"truncated with {current_length} steps at iter: {e}, and reward: {reward}")
                # next_state = self.translate_state(next_observation)
                is_picked_key = self._is_picked_key(game_state, action)
                next_state = self.get_state_from_obs(next_observation, is_picked_key=is_picked_key)
                # next_state = game_state.generate_successor(constants.Action(action))
                done = terminated or truncated
                self.update_q_table(game_state, action, reward, next_state)
                game_state = next_state
            self.decay_epsilon()
            episodes_length.append(current_length)
        print("[Statistics]: Avg_length {0}".format(sum(episodes_length) / len(episodes_length)))

        self.save_train_results(model_dir)

    def get_state_from_obs(self, observation, is_picked_key=False):
        game_map = self.translate_observation(observation['image'])
        # game_state = GameState(game_map, observation['direction'], goal_name="goal", goal_location=(6, 6))

        game_state = GameState(game_map, observation['direction'], is_picked_key=is_picked_key)
        return game_state

    def save_train_results(self, model_dir):
        file = open(model_dir + '/policy.csv', "w")
        fieldnames = ['state', 'action']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for state in self.visited_states:
            action, value = util.get_max_action(state, self.q_value_function)
            if value == 0 or action is None:
                action = -1
            else:
                action = action.value
            writer.writerow({'state': state, 'action': action})
        file.close()

    def translate_observation(self, raw_observation) -> List[List[str]]:
        """
            Gets a raw image of the game, and translates it to a list of lists of strings where each string the name of the cell it contains.
        """
        translated_image = [[] for _ in range(len(raw_observation[0]))]
        for row in raw_observation:
            translated_row = [IDX_TO_OBJECT[abs(box.tolist()[2])] for box in row]
            for i, val in enumerate(translated_row):  # for rotation
                translated_image[i].append(val)
        return translated_image

    def _is_picked_key(self, state, action):
        succ_is_picked_key = state.is_picked_key()
        if action == constants.Action.PICKUP.value:
            succ_is_picked_key = True

        if action == constants.Action.TOGGLE.value:
            succ_is_picked_key = False

        return succ_is_picked_key

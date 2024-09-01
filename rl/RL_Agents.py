import numpy as np
from collections import defaultdict
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


# class ValueIterationAgent:
#     """
#         * Please read learningAgents.py before reading this.*
#
#         A ValueIterationAgent takes a Markov decision process
#         (see mdp.py) on initialization and runs value iteration
#         for a given number of iterations using the supplied
#         discount factor.
#     """
#
#     def __init__(self, mdp, discount=0.9, iterations=100):
#         """
#           Your value iteration agent should take an mdp on
#           construction, run the indicated number of iterations
#           and then act according to the resulting policy.
#
#           Some useful mdp methods you will use:
#               mdp.getStates()
#               mdp.getPossibleActions(state)
#               mdp.getTransitionStatesAndProbs(state, action)
#               mdp.getReward(state, action, nextState)
#         """
#         self.mdp = mdp
#         self.discount = discount
#         self.iterations = iterations
#         self.values = util.Counter()  # A Counter is a dict with default 0
#         self.policy = {}
#
#         for i in range(iterations):
#             new_values = util.Counter()  # Store updated values for this iteration
#             for state in mdp.getStates():
#                 if mdp.isTerminal(state):
#                     continue  # Skip terminal states
#                 v_opt = float('-inf')
#                 best_actions = []
#
#                 for a in mdp.getPossibleActions(state):
#                     v_candidate = 0
#                     for next_state, prob in mdp.getTransitionStatesAndProbs(state, a):
#                         v_candidate += prob * (
#                                 mdp.getReward(state, a, next_state) + self.discount * self.values[next_state])
#
#                     if v_candidate > v_opt:
#                         v_opt = v_candidate
#                         best_actions = [a]  # Start a new list of best actions
#                     elif v_candidate == v_opt:
#                         best_actions.append(a)  # Add to the list of best actions
#
#                 new_values[state] = v_opt
#
#                 # Randomly select one of the best actions if there are ties
#                 self.policy[state] = np.random.choice(best_actions)
#
#             self.values = new_values  # Update the values with the newly computed ones
#
#     def getValue(self, state):
#         """
#           Return the value of the state (computed in __init__).
#         """
#         return self.values[state]
#
#     # def getQValue(self, state, action):
#     #     """
#     #       The q-value of the state action pair
#     #       (after the indicated number of value iteration
#     #       passes).  Note that value iteration does not
#     #       necessarily create this quantity and you may have
#     #       to derive it on the fly.
#     #     """
#     #     "*** YOUR CODE HERE ***"
#
#     def getPolicy(self, state):
#         """
#           The policy is the best action in the given state
#           according to the values computed by value iteration.
#           You may break ties any way you see fit.  Note that if
#           there are no legal actions, which is the case at the
#           terminal state, you should return None.
#         """
#         return self.policy[state]
#
#     def getAction(self, state):
#         "Returns the policy at the state (no exploration)."
#         return self.getPolicy(state)


class QLearningAgent:
    def __init__(self, env, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, alpha=0.0005):
        self.env = env
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.alpha = alpha
        self.q_table = np.zeros([env.observation_space.n, env.action_space.n])

    def act(self, state):
        if np.random.rand() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.q_table[state])

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_q_table(self, state, action, reward, next_state):
        q_value = self.q_table[state][action]
        next_q_value = np.max(self.q_table[next_state])
        self.q_table[state][action] = q_value + self.alpha * (reward + self.gamma * next_q_value - q_value)

    def learn(self, episodes):
        for e in range(episodes):
            observation, info = self.env.reset()
            state = self.translate_state(observation)
            done = False
            while not done:
                action = self.act(state)
                next_observation, reward, terminated, truncated, _ = self.env.step(action)
                next_state = self.translate_state(next_observation)
                done = terminated or truncated
                self.update_q_table(state, action, reward, next_state)
                state = next_state
            self.decay_epsilon()

    def translate_state(self, observation):
        """Translate the observation to a state tuple that can be used as a key in the Q-table."""
        agent_pos = tuple(observation['image'].flatten())  # Flatten the image to create a simple state representation
        direction = observation['direction']
        return agent_pos, direction


# class PPOAgent:
#     def __init__(self, env_name='MiniGrid-DistShift2-v0', n_envs=4, total_timesteps=100000):
#         self.env_name = env_name
#         self.env = gym.make(env_name)
#         self.vec_env = make_vec_env(lambda: gym.make(env_name), n_envs=n_envs)
#         self.model = PPO("MlpPolicy", self.vec_env, verbose=1)
#         self.total_timesteps = total_timesteps
#
#     def train(self):
#         """Train the PPO model."""
#         self.model.learn(total_timesteps=self.total_timesteps)
#         self.model.save(f"ppo_{self.env_name}")
#
#     def load(self, model_path):
#         """Load a pre-trained model."""
#         self.model = PPO.load(model_path, env=self.vec_env)
#
#     def act(self, observation):
#         """Predict the next action given an observation."""
#         action, _states = self.model.predict(observation, deterministic=True)
#         return action
#
#     def save(self, model_path):
#         """Save the model."""
#         self.model.save(model_path)
#
#     def load_and_run(self, model_path, n_episodes=5):
#         """Load a model and run it in the environment."""
#         self.load(model_path)
#         for episode in range(n_episodes):
#             observation, info = self.env.reset()
#             done = False
#             while not done:
#                 action = self.act(observation)
#                 observation, reward, terminated, truncated, info = self.env.step(action)
#                 done = terminated or truncated
#                 self.env.render()
#
#     def close(self):
#         """Close the environment."""
#         self.env.close()

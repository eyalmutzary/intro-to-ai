import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import gym


# Neural Network for the Q-Learning
class DQNNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


# ReplayMemory class
class ReplayMemory(object):
    '''
        Memory buffer for Experience Replay
    '''

    def __init__(self, capacity):
        '''
            Initialize a buffer containing max_size experiences
        '''
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def add(self, experience):
        '''
            Add an experience to the buffer
        '''
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = experience
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        '''
            Sample a batch of experiences from the buffer
        '''
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


# DQN Algorithm
class DQNAlgo:
    def __init__(self, env, state_size, action_size, device='cpu', max_memory=10000, discount=0.9, lr=0.001,
                 update_interval=1000,
                 batch_size=64):
        self.env = env
        self.device = device
        self.discount = discount
        self.batch_size = batch_size
        self.action_size = action_size

        # Policy and Target networks
        self.policy_network = DQNNetwork(state_size, action_size).to(self.device)
        self.target_network = DQNNetwork(state_size, action_size).to(self.device)
        self.target_network.load_state_dict(self.policy_network.state_dict())  # initialize with same weights

        # Exploration parameters
        self.epsilon = 0.9
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995
        self.update_target = update_interval
        self.steps_done = 0

        # Optimizer
        self.optimizer = optim.Adam(self.policy_network.parameters(), lr=lr)

        # Experience replay memory
        self.memory = ReplayMemory(max_memory)
        self.learn_step_counter = 0


def collect_experiences(self):
    obs = self.env.reset()
    done = False

    log_episodes = 0
    log_loss = []
    log_reward = []
    while not done:
        # prepocess obs
        preprocessed_obs = self.preprocess_obs([obs], device=self.device)
        # Predict the action
        sample = random.random()
        # eps_threshold = self.eps_end + (self.epsilon - self.eps_end) * \
        #     math.exp(-1. * self.steps_done / self.eps_decay)
        self.steps_done += 1
        if sample > self.epsilon:
            with torch.no_grad():
                Q = self.policy_network(preprocessed_obs)
            action = (Q == torch.max(Q)).nonzero()[:, 1]
            i = random.randrange(len(action))
            action = action[i].item()
        else:
            action = random.randrange(self.n_actions)

        # Apply action, get rewards and new state
        new_obs, reward, done, info = self.env.step(action)

        # Statistics
        log_reward.append(reward)
        log_episodes += 1

        # Store experience
        self.memory.add([obs, action, reward, new_obs, done])

        # update
        obs = new_obs

    # train model
    loss = self.train()
    log_loss.append(loss)

    return {
        "num_frames": log_episodes,
        "rewards": log_reward,
        "loss": log_loss,
        "won": info['success']
    }


def train(self):
    # load sample of memory
    if len(self.memory) < self.batch_size:
        batch = self.memory.sample(len(self.memory))
    else:
        batch = self.memory.sample(self.batch_size)

    # Zero the parameter gradients
    self.optimizer.zero_grad()

    # update target network if necessary
    if self.learn_step_counter % self.update_target == 0:
        self.update_target_network()

    # Q-Table
    Q_policy = torch.zeros(
        (len(batch), 1),
        device=self.device
    )
    Q_target = torch.zeros(
        (len(batch), 1),
        device=self.device
    )

    # preprocess obss
    obs = self.preprocess_obs(
        [exp[0] for exp in batch], device=self.device
    )
    new_obs = self.preprocess_obs(
        [exp[3] for exp in batch], device=self.device
    )

    # preprocess experience
    actions = [exp[1] for exp in batch]
    rewards = [exp[2] for exp in batch]
    dones = [exp[4] for exp in batch]

    # fill Q Table
    indices = np.arange(min(self.batch_size, len(self.memory)))
    Q_policy = self.policy_network(obs)[indices, actions]
    max_actions = self.target_network(new_obs).max(dim=1)[0]

    # Update Q-Table
    Q_target = torch.tensor(
        rewards, device=self.device
    ) + self.discount * max_actions
    # Q_target[dones] = 100.0

    # compute loss
    # loss = nn.MSELoss()(Q_policy, Q_target)
    loss = nn.functional.smooth_l1_loss(Q_policy, Q_target)
    loss.backward()
    self.optimizer.step()
    self.learn_step_counter += 1

    return loss.item()


def update_target_network(self):
    print("Target network update")
    self.target_network.load_state_dict(
        self.policy_network.state_dict()
    )

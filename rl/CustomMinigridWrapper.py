from __future__ import annotations

from typing import SupportsFloat

import gym
from gym import spaces
import numpy as np
from gymnasium import logger, spaces
from gymnasium.core import ActionWrapper, ObservationWrapper, ObsType, Wrapper, ActType, WrapperActType


from minigrid.core.constants import COLOR_TO_IDX, OBJECT_TO_IDX, STATE_TO_IDX
from minigrid.core.world_object import Goal

'''
This class is a custom wrapper for the MiniGrid environment. 
Its observation method mimics the SymbolicObsWrapper (just to implement the image observation CAN BE CHANGED according 
to needs), adds functionality to the step method to automatically move the agent forward after turning left or right,
and removes the default visualization of the partially observable field of view in the render method.
'''


class CustomMinigridWrapper(ObservationWrapper):

    def __init__(self, env):
        super().__init__(env)

        new_image_space = spaces.Box(
            low=0,
            high=max(OBJECT_TO_IDX.values()),
            shape=(self.env.width, self.env.height, 3),  # number of cells
            dtype="uint8",
        )
        self.observation_space = spaces.Dict(
            {**self.observation_space.spaces, "image": new_image_space}
        )

    def observation(self, obs):
        objects = np.array(
            [OBJECT_TO_IDX[o.type] if o is not None else -1 for o in self.grid.grid]
        )
        agent_pos = self.env.agent_pos
        ncol, nrow = self.width, self.height
        grid = np.mgrid[:ncol, :nrow]
        _objects = np.transpose(objects.reshape(1, nrow, ncol), (0, 2, 1))

        grid = np.concatenate([grid, _objects])
        grid = np.transpose(grid, (1, 2, 0))
        grid[agent_pos[0], agent_pos[1], 2] = OBJECT_TO_IDX["agent"]
        obs["image"] = grid

        return obs

    def reward(self, reward):
        # Custom reward function: Encouraging fewer steps to reach the goal
        return 1 - 0.9 * (self.step_count / self.max_steps)

    def step(self, action):
        """
        Modifies the step function such that if the action is turn left or right,
        the agent automatically moves forward as well, and doubles the reward accordingly.
        """
        # Check the action for turning left or right
        left_action = 0
        right_action = 1
        forward_action = 2

        if action == left_action or action == right_action:
            # First, perform the turn (left or right)
            next_observation, reward, terminated, truncated, info = self.env.step(action)
            # Then, immediately move forward
            next_observation, forward_reward, terminated, truncated, info = self.env.step(forward_action)

            # Combine the rewards (double for the turn + move combo)
            total_reward = reward + forward_reward
        else:
            # If the action is not a turn (it's just moving forward or something else), act normally
            next_observation, total_reward, terminated, truncated, info = self.env.step(action)

        return next_observation, total_reward, terminated, truncated, info

    def render(self, *args, **kwargs):
        """This removes the default visualization of the partially observable field of view."""
        kwargs['highlight'] = False
        return self.unwrapped.render(*args, **kwargs)


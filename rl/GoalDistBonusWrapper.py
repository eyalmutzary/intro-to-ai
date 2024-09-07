from __future__ import annotations

from typing import SupportsFloat, Any

import gym
from gym import spaces
import numpy as np
from gymnasium import logger, spaces
from gymnasium.core import ActionWrapper, ObservationWrapper, ObsType, Wrapper, ActType, WrapperActType, WrapperObsType

from minigrid.core.constants import COLOR_TO_IDX, OBJECT_TO_IDX, STATE_TO_IDX
from minigrid.core.world_object import Goal


class GoalDistBonusWrapper(ObservationWrapper):

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[
        WrapperObsType, dict[str, Any]]:
        return super().reset(seed=seed, options=options)

    def step(self, action: ActType) -> tuple[WrapperObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        self.step_count += 1
        reward = -1
        terminated = False
        truncated = False

        # Get the position in front of the agent
        fwd_pos = self.front_pos

        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)

        # Rotate left
        if action == self.actions.left:
            self.agent_dir -= 1
            if self.agent_dir < 0:
                self.agent_dir += 4

        # Rotate right
        elif action == self.actions.right:
            self.agent_dir = (self.agent_dir + 1) % 4

        # Move forward
        elif action == self.actions.forward:
            if fwd_cell is None or fwd_cell.can_overlap():
                self.agent_pos = tuple(fwd_pos)
            if fwd_cell is not None and fwd_cell.type == "goal":
                terminated = True
                reward = self._reward()
            if fwd_cell is not None and fwd_cell.type == "lava":
                reward = -10
                terminated = True

        # Pick up an object
        elif action == self.actions.pickup:
            if fwd_cell and fwd_cell.can_pickup():
                if self.carrying is None:
                    self.carrying = fwd_cell
                    self.carrying.cur_pos = np.array([-1, -1])
                    self.grid.set(fwd_pos[0], fwd_pos[1], None)

        # Drop an object
        elif action == self.actions.drop:
            if not fwd_cell and self.carrying:
                self.grid.set(fwd_pos[0], fwd_pos[1], self.carrying)
                self.carrying.cur_pos = fwd_pos
                self.carrying = None

        # Toggle/activate an object
        elif action == self.actions.toggle:
            if fwd_cell:
                fwd_cell.toggle(self, fwd_pos)

        # Done action (not used by default)
        elif action == self.actions.done:
            pass

        else:
            raise ValueError(f"Unknown action: {action}")

        if self.step_count >= self.max_steps:
            truncated = True
            reward = self._truncatedReward()

        if self.render_mode == "human":
            self.render()

        obs = self.gen_obs()

        return obs, reward, terminated, truncated, {}

    def _reward(self) -> float:
        """
        Compute the reward to be given upon success, scaled based on steps taken.
        The reward starts high and decreases as the step count increases.
        """
        base_reward = 100  # Start with a higher reward
        step_penalty = 0.9 * (self.step_count / self.max_steps)
        return base_reward * (1 - step_penalty)

    def _truncatedReward(self) -> float:
        base_reward = 1
        obs = self.env.observation_space
        # Assuming OBJECT_TO_IDX has a key "goal" representing the goal's index
        goal_idx = OBJECT_TO_IDX["goal"]

        # The grid's third dimension (index 2) contains the object indices
        object_layer = obs["image"][:, :, 2]

        # Find the position where the grid value matches the goal's index
        goal_position = np.argwhere(object_layer == goal_idx)

        return

    def observation(self, observation: ObsType) -> WrapperObsType:
        pass

from __future__ import annotations

from typing import SupportsFloat, Any

import numpy as np
from gymnasium.core import ActType, ObsType
from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall, Lava
from minigrid.minigrid_env import MiniGridEnv


class LavaMazeEnv(MiniGridEnv):
    def __init__(
            self,
            size=8,
            agent_start_pos=(1, 1),
            agent_start_dir=0,
            max_steps: int | None = None,
            **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 5 * size ** 2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "navigate through the lava maze to reach the goal"

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Create a lava maze pattern
        for i in range(1, height - 1):
            # Place lava on some rows
            if i % 2 == 0:
                for j in range(1, width - 1):
                    if j % 3 == 0:  # Lava on every second tile
                        self.grid.set(j, i, Lava())
                        if i == 2:
                            self.grid.set(j-1, i, Lava())

        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "navigate through the lava maze to reach the goal"
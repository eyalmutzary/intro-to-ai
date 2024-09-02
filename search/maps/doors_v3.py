from __future__ import annotations

from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall, Lava
from minigrid.minigrid_env import MiniGridEnv


class DoorsV3Env(MiniGridEnv):
    def __init__(
        self,
        size=15,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "grand mission"

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Generate vertical separation wall
        for i in range(0, height):
            self.grid.set(7, i, Wall())
            
        for i in range(0, width):
            self.grid.set(i, 7, Wall())
        
        # Place the door and key
        self.grid.set(7, 2, Door(COLOR_NAMES[0], is_locked=True))
        self.grid.set(2, 5, Key(COLOR_NAMES[0]))
        
        self.grid.set(9, 7, Door(COLOR_NAMES[1], is_locked=True))
        self.grid.set(12, 1, Key(COLOR_NAMES[1]))
        
        self.grid.set(7, 12, Door(COLOR_NAMES[3], is_locked=True))
        self.grid.set(12, 13, Key(COLOR_NAMES[3]))
        
        # Add some lava
        for i in range(2, 7):
            self.grid.set(3, i, Lava())
            
        # for i in range(0,3):
        #     self.grid.set(2+i, 10+i, Lava())
        for i in range(0,3):
            for j in range(0,4):
                self.grid.set(2+i, 10+j, Lava())
        
        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), 1, height - 2)

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"
        
from __future__ import annotations

from typing import SupportsFloat, Any

from gym.core import ActType, ObsType
from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall, Lava
from minigrid.minigrid_env import MiniGridEnv


class DoorsV1Env(MiniGridEnv):
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
            self.grid.set(3, i, Wall())

        # Place the door and key
        self.grid.set(3, 2, Door(COLOR_NAMES[0], is_locked=True))
        self.grid.set(1, 4, Key(COLOR_NAMES[0]))

        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        self.grid.set(4, 3, Lava())
        self.grid.set(5, 5, Lava())

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"

    # def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
    #     self.step_count += 1
    #
    #     reward = 0
    #     terminated = False
    #     truncated = False
    #
    #     # Get the position in front of the agent
    #     fwd_pos = self.front_pos
    #
    #     # Get the contents of the cell in front of the agent
    #     fwd_cell = self.grid.get(*fwd_pos)
    #
    #     # Rotate left
    #     if action == self.actions.left:
    #         self.agent_dir -= 1
    #         if self.agent_dir < 0:
    #             self.agent_dir += 4
    #
    #     # Rotate right
    #     elif action == self.actions.right:
    #         self.agent_dir = (self.agent_dir + 1) % 4
    #
    #     # Move forward
    #     elif action == self.actions.forward:
    #         if fwd_cell is None or fwd_cell.can_overlap():
    #             self.agent_pos = tuple(fwd_pos)
    #         if fwd_cell is not None and fwd_cell.type == "goal":
    #             terminated = True
    #             reward = self._reward()
    #         if fwd_cell is not None and fwd_cell.type == "lava":
    #             reward = -10
    #             terminated = True
    #
    #     # Pick up an object
    #     elif action == self.actions.pickup:
    #         if fwd_cell and fwd_cell.can_pickup():
    #             if self.carrying is None:
    #                 self.carrying = fwd_cell
    #                 self.carrying.cur_pos = np.array([-1, -1])
    #                 self.grid.set(fwd_pos[0], fwd_pos[1], None)
    #
    #     # Drop an object
    #     elif action == self.actions.drop:
    #         if not fwd_cell and self.carrying:
    #             self.grid.set(fwd_pos[0], fwd_pos[1], self.carrying)
    #             self.carrying.cur_pos = fwd_pos
    #             self.carrying = None
    #
    #     # Toggle/activate an object
    #     elif action == self.actions.toggle:
    #         if fwd_cell:
    #             fwd_cell.toggle(self, fwd_pos)
    #
    #     # Done action (not used by default)
    #     elif action == self.actions.done:
    #         pass
    #
    #     else:
    #         raise ValueError(f"Unknown action: {action}")
    #
    #     if self.step_count >= self.max_steps:
    #         truncated = True
    #
    #
    #     if self.render_mode == "human":
    #         self.render()
    #
    #     obs = self.gen_obs()
    #     return obs, reward, terminated, truncated, {}

# def main():
#     from minigrid.manual_control import ManualControl

#     env = DoorSimple(render_mode="human")

#     # enable manual control for testing
#     manual_control = ManualControl(env, seed=42)
#     manual_control.start()

    
# if __name__ == "__main__":
#     main()
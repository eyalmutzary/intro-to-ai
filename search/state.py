
from enum import Enum
from typing import List, Tuple
import copy
from constants import BLOCKED_CELLS, Direction, Action


class GameState:
    def __init__(self, observation, goal_location, player_direction=Direction.RIGHT.value):
        self._observation = observation
        self._player_direction: int = player_direction 
        self._goal_location = goal_location
        self._player_location: Tuple[int, int] = self._get_player_location()

    @property
    def observation(self):
        return self._observation
    
    @property
    def player_location(self):
        return self._player_location
    
    @property
    def goal_location(self):
        return self._goal_location

    def get_legal_actions(self) -> List[Action]:        
        forward_row, forward_col = self._get_forward_location()
        forward_cell = self.observation[forward_row][forward_col]
        
        right_row, right_col = self._get_right_location()
        right_cell = self.observation[right_row][right_col]
        
        left_row, left_col = self._get_left_location()
        left_cell = self.observation[left_row][left_col]
        
        legal_actions = []
        if forward_cell not in BLOCKED_CELLS:
            legal_actions.append(Action.MOVE_FORWARD)
        if right_cell not in BLOCKED_CELLS:
            legal_actions.append(Action.TURN_RIGHT)
        if left_cell not in BLOCKED_CELLS:
            legal_actions.append(Action.TURN_LEFT)

        return legal_actions
    
    def generate_successor(self, action: Action) -> 'GameState':
        succ = GameState(copy.deepcopy(self._observation), self._goal_location, self._player_direction) 
        
        if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
            succ._rotate_player(action)
        
        succ._move_player_forward()

        return succ
    
    def _get_player_location(self) -> Tuple[int, int]:
        for i, row in enumerate(self._observation):
            for j, cell in enumerate(row):
                if cell == 'agent':
                    return (i, j)
        raise ValueError("Player location not found in observation")
    
    def _rotate_player(self, action: Action) -> None:
        if action == Action.TURN_LEFT:
            self._player_direction = (self._player_direction - 1) % 4
        elif action == Action.TURN_RIGHT:
            self._player_direction = (self._player_direction + 1) % 4
        else:
            raise ValueError(f"Invalid action: {action}")
    
    def _move_player_forward(self) -> None:
        old_row, old_col = self._player_location
        new_row, new_col = self._get_forward_location()
        self._observation[old_row][old_col] = 'empty'
        self._observation[new_row][new_col] = 'agent'
        self._player_location = self._get_player_location()

    
    def _get_forward_location(self):
        if self._player_direction == Direction.RIGHT.value:
            return (self._player_location[0], self._player_location[1] + 1)
        elif self._player_direction == Direction.DOWN.value:
            return (self._player_location[0] + 1, self._player_location[1])
        elif self._player_direction == Direction.LEFT.value:
            return (self._player_location[0], self._player_location[1] - 1)
        elif self._player_direction == Direction.UP.value:
            return (self._player_location[0] - 1, self._player_location[1])
        else:
            raise ValueError(f"Invalid player direction: {self._player_direction}")
    
    def _get_left_location(self):
        if self._player_direction == Direction.RIGHT.value:
            return (self._player_location[0] - 1, self._player_location[1])
        elif self._player_direction == Direction.DOWN.value:
            return (self._player_location[0], self._player_location[1] + 1)
        elif self._player_direction == Direction.LEFT.value:
            return (self._player_location[0] + 1, self._player_location[1])
        elif self._player_direction == Direction.UP.value:
            return (self._player_location[0], self._player_location[1] - 1)
        else:
            raise ValueError(f"Invalid player direction: {self._player_direction}")
        
    def _get_right_location(self):
        if self._player_direction == Direction.RIGHT.value:
            return (self._player_location[0] + 1, self._player_location[1])
        elif self._player_direction == Direction.DOWN.value:
            return (self._player_location[0], self._player_location[1] - 1)
        elif self._player_direction == Direction.LEFT.value:
            return (self._player_location[0] - 1, self._player_location[1])
        elif self._player_direction == Direction.UP.value:
            return (self._player_location[0], self._player_location[1] + 1)
        else:
            raise ValueError(f"Invalid player direction: {self._player_direction}")
        
    def __str__(self) -> str:
        obs_map = ""
        for row in self._observation:
            obs_map += " ".join(row) + "\n"
        direction_str = Direction(self._player_direction).name
        return f"""Player location: {self._player_location}, Player direction: {direction_str}\n{obs_map}
                """
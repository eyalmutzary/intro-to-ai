from enum import Enum
from typing import List, Tuple
import copy
from constants import BLOCKED_CELLS, Direction, Action, DIRECTION_VECTORS

class GameState:
    def __init__(self, game_map, goal_location, player_direction=Direction.RIGHT.value):
        self._game_map = game_map
        self._player_direction: int = player_direction 
        self._goal_location = goal_location
        self._player_location: Tuple[int, int] = self._get_player_location()

    @property
    def game_map(self):
        return self._game_map
    
    @property
    def player_direction(self):
        return self._player_direction
    
    @property
    def goal_location(self):
        return self._goal_location
    
    @property
    def player_location(self):
        return self._player_location

    def get_legal_actions(self) -> List[Action]:        
        legal_actions = []

        if self._is_cell_free(self._get_new_location(self._player_direction)):
            legal_actions.append(Action.MOVE_FORWARD)

        if self._is_cell_free(self._get_new_location(self._get_rotated_direction(Action.TURN_RIGHT))):
            legal_actions.append(Action.TURN_RIGHT)

        if self._is_cell_free(self._get_new_location(self._get_rotated_direction(Action.TURN_LEFT))):
            legal_actions.append(Action.TURN_LEFT)

        return legal_actions
    
    def generate_successor(self, action: Action):
        succ_new_direction = self._player_direction
        if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
            succ_new_direction = self._get_rotated_direction(action)
            
        succ = GameState(copy.deepcopy(self._game_map), self._goal_location, succ_new_direction) 
        succ._move_player_forward()

        return succ
    
    def _get_player_location(self) -> Tuple[int, int]:
        for i, row in enumerate(self._game_map):
            for j, cell in enumerate(row):
                if cell == 'agent':
                    return (i, j)
        raise ValueError("Player location not found in game map")
    
    def _get_rotated_direction(self, action: Action) -> None:
        if action == Action.TURN_LEFT:
            return (self._player_direction - 1) % 4
        elif action == Action.TURN_RIGHT:
            return (self._player_direction + 1) % 4
        else:
            raise ValueError(f"Invalid action: {action}")
    
    def _move_player_forward(self) -> None:
        old_row, old_col = self._player_location
        new_row, new_col = self._get_new_location(self._player_direction)
        self._game_map[old_row][old_col] = 'empty'
        self._game_map[new_row][new_col] = 'agent'
        self._player_location = (new_row, new_col)

    def _get_new_location(self, direction: int) -> Tuple[int, int]:
        row_offset, col_offset = DIRECTION_VECTORS[direction]
        return (self._player_location[0] + row_offset, self._player_location[1] + col_offset)

    def _is_cell_free(self, location: Tuple[int, int]) -> bool:
        row, col = location
        return self._game_map[row][col] not in BLOCKED_CELLS
    
    def __str__(self) -> str:
        obs_map = ""
        for row in self._game_map:
            obs_map += " ".join(row) + "\n"
        direction_str = Direction(self._player_direction).name
        return f"""Player location: {self._player_location}, Player direction: {direction_str}\n{obs_map}
                """

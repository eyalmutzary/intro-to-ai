from enum import Enum
from typing import List, Tuple
import copy
from constants import BLOCKED_CELLS, Direction, Action, DIRECTION_VECTORS
from collections import deque

class GameState:
    def __init__(self, game_map, player_direction=Direction.RIGHT.value, is_picked_key=False, goal_name=None, goal_location=None):
        player_location = GameState._get_player_location(game_map)
        if not goal_name or not goal_location:
            goal_name, goal_location = GameState._find_next_target(game_map, player_location, is_picked_key)
        
        self._game_map = game_map
        self._player_direction: int = player_direction 
        self._player_location: Tuple[int, int] = player_location
        self._is_picked_key = is_picked_key
        self._goal_location = goal_location
        self._goal_name = goal_name

    @property
    def game_map(self):
        return self._game_map
    
    @property
    def player_direction(self):
        return self._player_direction
    
    @property
    def player_location(self):
        return self._player_location
    
    @property
    def goal_location(self):
        return self._goal_location

    @property
    def goal_name(self):
        return self._goal_name

    def get_legal_actions(self) -> List[Action]:        
        legal_actions = []

        forward_row, forward_col = self._get_new_location(self._player_direction)
        if self._is_cell_free((forward_row, forward_col)):
            legal_actions.append(Action.MOVE_FORWARD)
            
        if self._is_cell_free(self._get_new_location(self._get_rotated_direction(Action.TURN_RIGHT))):
            legal_actions.append(Action.TURN_RIGHT)

        if self._is_cell_free(self._get_new_location(self._get_rotated_direction(Action.TURN_LEFT))):
            legal_actions.append(Action.TURN_LEFT)

        if self._game_map[forward_row][forward_col] == 'key':
            legal_actions.append(Action.PICKUP)
        
        if self._game_map[forward_row][forward_col] == 'door':
            legal_actions.append(Action.TOGGLE)
        
        return legal_actions
    
    def generate_successor(self, action: Action):
        succ_new_direction = self._player_direction
        if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
            succ_new_direction = self._get_rotated_direction(action)
        
        succ_is_picked_key = self._is_picked_key
        if action == Action.PICKUP:
            succ_is_picked_key = True
        
        if action == Action.TOGGLE:
            succ_is_picked_key = False # ! might cause a bug in case of multiple doors and keys of different colors 
        
        succ = GameState(copy.deepcopy(self._game_map),
                        succ_new_direction, 
                        is_picked_key=succ_is_picked_key,
                        goal_name=self._goal_name,
                        goal_location=self._goal_location
                        ) 
        succ._move_player_forward()
        return succ
    
    @staticmethod
    def _get_player_location(game_map: List[List[str]]) -> Tuple[int, int]:
        for i, row in enumerate(game_map):
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
    
    @staticmethod
    def _find_next_target(game_map: List[List[str]], player_location, is_picked_key) -> tuple:
        rows, cols = len(game_map), len(game_map[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        queue = deque([player_location])
        visited = set()
        visited.add(player_location)
        
        found_goal = None
        found_key = None
        found_door = None
        
        while queue:
            r, c = queue.popleft()
            
            # Check and mark if we found any of the targets
            if game_map[r][c] == 'goal':
                found_goal = (r, c)
            elif game_map[r][c] == 'key':
                found_key = (r, c)
            elif game_map[r][c] == 'door':
                found_door = (r, c)
            
            # Explore neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check if the neighbor is within bounds and is not a wall or visited
                if 0 <= nr < rows and 0 <= nc < cols and game_map[nr][nc] not in ['wall', 'lava'] and (nr, nc) not in visited:
                    if game_map[nr][nc] == 'door': # a door could be a target, but it should not be passable
                        found_door = (nr, nc)
                        continue
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        # Return based on priority
        if found_goal:
            return ('goal', found_goal)
        elif found_key and not is_picked_key:
            return ('key', found_key)
        elif found_door and is_picked_key:
            return ('door', found_door)
        else:
            raise ValueError("No target found in the current game state:" + str(game_map))
    
    
    def __str__(self) -> str:
        obs_map = ""
        for row in self._game_map:
            obs_map += " ".join(row) + "\n"
        direction_str = Direction(self._player_direction).name
        return f"""Player location: {self._player_location}, Player direction: {direction_str}\n{obs_map}
                """

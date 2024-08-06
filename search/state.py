
from enum import Enum
from typing import List, Tuple
import copy


class Action(Enum):
    TURN_LEFT = 0
    TURN_RIGHT = 1
    MOVE_FORWARD = 2

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    

class GameState:
    def __init__(self, observation, player_direction=Direction.RIGHT.value):
        # * Note: the direction and location is relative to the observation and not the actual environment
        self._observation = observation
        self._player_direction: int = player_direction 
        self._player_location: Tuple[int, int] = self._get_player_location()

    @property
    def observation(self):
        return self._observation
    
    @property
    def player_location(self):
        return self._player_location

    def get_legal_actions(self) -> List[Action]:        
        legal_actions = [Action.TURN_LEFT, Action.TURN_RIGHT]
        
        forward_location = self.get_forward_location()
        # # check if the forward location is out of bounds of the observation
        # if forward_location[0] < 0 or forward_location[0] >= len(self.observation) or forward_location[1] < 0 or forward_location[1] >= len(self.observation[0]):
        #     return legal_actions
        
        forward_cell = self.observation[forward_location[0]][forward_location[1]]
        if forward_cell != 'wall':
            legal_actions.append(Action.MOVE_FORWARD)

        return legal_actions
    
    def generate_successor(self, action: Action) -> 'GameState':
        succ_direction = self._player_direction
        succ_observation = copy.deepcopy(self._observation)
        
        if action == Action.TURN_LEFT:
            self._player_direction = (self._player_direction - 1) % 4
        elif action == Action.TURN_RIGHT:
            self._player_direction = (self._player_direction + 1) % 4
        elif action == Action.MOVE_FORWARD:
            self._move_player_forward(succ_observation)
        else:
            raise ValueError(f"Invalid action: {action}")

        return GameState(succ_observation, succ_direction) 
    
    
    def _get_player_location(self) -> Tuple[int, int]:
        for i, row in enumerate(self._observation):
            for j, cell in enumerate(row):
                if cell == 'agent':
                    return (i, j)
        raise ValueError("Player location not found in observation")
    
    
    def _move_player_forward(self, new_observation: List[List[str]]) -> None:
        old_row, old_col = self._player_location
        new_row, new_col = self.get_forward_location()
        new_observation[old_row][old_col] = 'empty'
        new_observation[new_row][new_col] = 'agent'

    
    def get_forward_location(self):
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
        
        
    def __str__(self) -> str:
        obs_map = ""
        for row in self._observation:
            obs_map += " ".join(row) + "\n"
        direction_str = Direction(self._player_direction).name
        return f"""Player location: {self._player_location}, Player direction: {direction_str}\n{obs_map}
                """
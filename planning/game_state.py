
from enum import Enum
from minigrid.core.constants import IDX_TO_OBJECT
from typing import List, Tuple

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
    def __init__(self, raw_observation, player_location=None, player_direction=0):
        # * Note: the direction and location is relative to the observation and not the actual environment
        self._raw_observation = raw_observation
        self._observation: List[List[str]] = self._translate_observation(raw_observation)
        if player_location is not None:
            self._player_location: Tuple[int, int] = player_location
        else:
            self._player_location: Tuple[int, int] = self._get_default_player_location_in_observation()
        self._player_direction: int = player_direction  # * 0: right, 1: down, 2: left, 3: up

    @property
    def observation(self):
        return self._observation
    
    @property
    def player_location(self):
        return self._player_location

    def get_legal_actions(self) -> List[Action]:        
        legal_actions = [Action.TURN_LEFT, Action.TURN_RIGHT]
        
        forward_location = self.get_forward_location()
        # check if the forward location is out of bounds of the observation
        if forward_location[0] < 0 or forward_location[0] >= len(self.observation) or forward_location[1] < 0 or forward_location[1] >= len(self.observation[0]):
            return legal_actions
        
        forward_cell = self.observation[forward_location[0]][forward_location[1]]
        if forward_cell != 'wall':
            legal_actions.append(Action.MOVE_FORWARD)

        return legal_actions
    
    def generate_successor(self, action: Action) -> 'GameState':
        # TODO: should change the player location accordingly
        if action == Action.TURN_LEFT:
            self._player_direction = (self._player_direction - 1) % 4
        elif action == Action.TURN_RIGHT:
            self._player_direction = (self._player_direction + 1) % 4
        elif action == Action.MOVE_FORWARD:
            self._player_location =  self.get_forward_location()
        else:
            raise ValueError(f"Invalid action: {action}")

        return GameState(self._raw_observation, self._player_location, self._player_direction)
        
    
    def _translate_observation(self, raw_observation) -> None:
        processed_observation = []
        for row in raw_observation:
            processed_observation.append([])
            for box in row:
                processed_observation[-1].insert(0, IDX_TO_OBJECT[box.tolist()[0]])
        return processed_observation
        
    
    def _get_default_player_location_in_observation(self) -> Tuple[int, int]:
        observation_size = len(self._observation)
        return (observation_size//2, 0)
    
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

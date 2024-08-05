
from enum import Enum
from minigrid.core.constants import IDX_TO_OBJECT
from typing import List, Tuple

class Action(Enum):
    TURN_LEFT = 1
    TURN_RIGHT = 2
    MOVE_FORWARD = 3


class GameState:
    def __init__(self, raw_observation):
        self._observation: List[List[str]] = self._translate_observation(raw_observation)
        self._observation_size: int = len(raw_observation)
        self._player_location: Tuple[int, int] = self._get_player_location_in_observation()

    @property
    def observation(self):
        return self._observation
    
    @property
    def observation_size(self):
        return self._observation_size

    def get_legal_actions(self) -> List[Action]:
        forward_cell = self._observation[self._player_location[0]][self._player_location[1] + 1]
        legal_actions = [Action.TURN_LEFT, Action.TURN_RIGHT]
        if forward_cell == 'wall':
            legal_actions.append(Action.MOVE_FORWARD)
        return legal_actions
    
    def _translate_observation(self, raw_observation) -> None:
        processed_observation = []
        for row in raw_observation:
            processed_observation.append([])
            for box in row:
                processed_observation[-1].insert(0, IDX_TO_OBJECT[box.tolist()[0]])
        return processed_observation
        
    
    def _get_player_location_in_observation(self) -> Tuple[int, int]:
        return (self._observation_size//2, 0)
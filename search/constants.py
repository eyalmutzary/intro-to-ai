from enum import Enum

GAME_MAPS = [
    'MiniGrid-Empty-8x8-v0',
    'MiniGrid-Empty-16x16-v0',
    'MiniGrid-Empty-Random-6x6-v0',
    'MiniGrid-LavaGapS7-v0',
    'MiniGrid-DistShift2-v0',
]

class Action(Enum):
    TURN_LEFT = 0
    TURN_RIGHT = 1
    MOVE_FORWARD = 2

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    
BLOCKED_CELLS = ['wall', 'lava']


# Used to rotate the player in the grid
DIRECTION_VECTORS = {
    Direction.RIGHT.value: (0, 1),
    Direction.DOWN.value: (1, 0),
    Direction.LEFT.value: (0, -1),
    Direction.UP.value: (-1, 0)
}
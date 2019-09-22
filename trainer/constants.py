from enum import Enum

EMPTY_CELL = 0
WALL = 1
PLAYER_ON_EMPTY_CELL = 2
PORTAL = 3
PLAYER_ON_PORTAL = 5
ENEMY_ANT = 6
ENEMY_ANT_ON_PORTAL = 7

PLAYER_CONTAINER_CELLS = [PLAYER_ON_EMPTY_CELL, PLAYER_ON_PORTAL]
PLAYER_MOVABLE_CELLS = [EMPTY_CELL, PORTAL]
ENEMY_MOVABLE_CELLS = [EMPTY_CELL, PLAYER_ON_EMPTY_CELL]
ENEMY_CONTAINER_CELLS = [ENEMY_ANT, ENEMY_ANT_ON_PORTAL]

# [cur][target]
# [target][cur]
MOVE_MAPPING = {
    6: { 0: 6, 3: 7, 2: 6, 6: 6},
    0: { 6: 0, 7: 3 },
    3: { 6: 0 },
    2: { 6: 6, 7: 3 },
    7: { 0: 6, 2: 6 }
}

class PlayerAction(Enum):
    UP    = [ 0, -1]
    RIGHT = [ 1,  0]
    DOWN  = [ 0,  1]
    LEFT  = [-1,  0]

ACTIONS = [PlayerAction.UP, PlayerAction.RIGHT, PlayerAction.DOWN, PlayerAction.LEFT]

class GameStatus(Enum):
    ONGOING = 0
    PLAYER_WON = 1
    PLAYER_LOST = 2

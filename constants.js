export const CELL_SIZE = 40
export const GAME_WIDTH = 480
export const GAME_HEIGHT = 320

export const EMPTY_CELL = 0              // 0: empty cell
export const WALL = 1                    // 1: wall
export const PLAYER_ON_EMPTY_CELL = 2    // 2: empty cell with player on it
export const PORTAL = 3                  // 3: portal
export const NON_CELL = 4                // 4: no-func cell for now
export const PLAYER_ON_PORTAL = 5        // 5: portal with player on it
export const ENEMY_ANT = 6               // 6: ant
export const ENEMY_ANT_ON_PORTAL = 7     // 7: portal with ant on it

export const PLAYER_MOVABLE_CELLS = [
  EMPTY_CELL, PORTAL
]

export const PLAYER_CONTAINER_CELLS = [
  PLAYER_ON_EMPTY_CELL, PLAYER_ON_PORTAL
]

export const ENEMY_CELLS = [
  ENEMY_ANT
]

export const ENEMT_MOVABLE_CELLS = [
  EMPTY_CELL, PLAYER_ON_EMPTY_CELL, PORTAL
]

// cell transitions
export const PLAYER_MOVE_CELL_TRANSITIONS = {
  2 : 0, // empty cell with player -> empty player
  0 : 2, // empty cell -> empty cell with player on it
  3 : 5, // portal -> portal with player on it
  5 : 3  // portal with player -> portal
}

export const ENEMY_ANT_MOVE_CELL_TRANSITIONS = {
  // 
}

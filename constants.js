export const CELL_SIZE = 40
export const GAME_WIDTH = 480
export const GAME_HEIGHT = 320

// 0: empty cell
// 1: wall
// 2: empty cell with player on it
// 3: portal
// 4: no-func cell for now
// 5: portal with player on it
// 6: ant
export const PLAYER_MOVABLE_CELLS = [
  0, 3
]
export const PLAYER_CONTAINER_CELLS = [
  2, 5
]
export const ENEMY_CELLS = [
  6
]
export const ENEMT_MOVABLE_CELLS = [
  0, 2, 3
]

// cell transitions
export const PLAYER_MOVE_CELL_TRANSITIONS = {
  2 : 0, // empty cell with player -> empty player
  0 : 2, // empty cell -> empty cell with player on it
  3 : 5, // portal -> portal with player on it
  5 : 3  // portal with player -> portal
}

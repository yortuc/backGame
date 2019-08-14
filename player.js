import { 
    PLAYER_MOVABLE_CELLS, 
    PLAYER_MOVE_CELL_TRANSITIONS,
    PLAYER_CONTAINER_CELLS 
} from './constants.js'

export const tryMovePlayer = (map, move, playerMovedCallback) => {
    const {x, y} = getPlayerPosFromMap(map)
    
    if(move.x){
        const _x = x + move.x
        if(_x >= 0 && _x < map[0].length && PLAYER_MOVABLE_CELLS.includes(map[y][_x])){
          const currentCellId = map[y][x]
          const targetCellId = map[y][_x]
          map[y][_x] = PLAYER_MOVE_CELL_TRANSITIONS[targetCellId]
          map[y][x] = PLAYER_MOVE_CELL_TRANSITIONS[currentCellId]
          playerMovedCallback(currentCellId, targetCellId)
        }
    }
    
    if(move.y){
        const _y = y + move.y
        if(_y >= 0 && _y < map.length && PLAYER_MOVABLE_CELLS.includes(map[_y][x])){
          const currentCellId = map[y][x]
          const targetCellId = map[_y][x]
          map[_y][x] = PLAYER_MOVE_CELL_TRANSITIONS[targetCellId]
          map[y][x] = PLAYER_MOVE_CELL_TRANSITIONS[currentCellId]
          playerMovedCallback(currentCellId, targetCellId)
        }
    }
  }
  

export const getPlayerPosFromMap = (map) => {
    for(let j=0; j<map.length; j++){
      for(let i=0; i<map.length; i++){
        const cellId = map[j][i]
        if(PLAYER_CONTAINER_CELLS.includes(cellId)) {
          return {x: i, y:j, id: cellId}
        }
      }
    }
  }
  
   
import { 
  CELL_SIZE, 
  ENEMY_CELLS, 
  PLAYER_CONTAINER_CELLS, 
  PORTAL 
} from './constants.js'

import { map1, map2 } from './maps.js'
import { renderGame } from './mapRenderer.js'
import { tryMovePlayer } from './player.js'
import { findPath } from './pathFinding.js'

const c = document.getElementById("c").getContext("2d")

const maps = [map1, map2]

let mapIndex = 0
let currentMap = maps[0]

let startTime = null
let elapsedTime = 0

let currentScore = {
  level: 1,
  health: 100,
  moves: 0,
  enemiesAlive: 2,
  keysCollected: 0
}

let pathWays = [[]]

 
const enemyPositionsFromMap = (map) => {
  let enemies = []
  for(let j=0; j<map.length; j++){
    for(let i=0; i<map[0].length; i++){
      if(ENEMY_CELLS.includes(map[j][i])){
        enemies.push({y: j, x:i, id: map[j][i]})
      }
    }
  }
  return enemies
}

const playerPosFromMap = (map) => {
  for(let j=0; j<map.length; j++){
    for(let i=0; i<map[0].length; i++){
      if(PLAYER_CONTAINER_CELLS.includes(map[j][i])){
        return {y: j, x:i, id: map[j][i]}
      }
    }
  }
}

const moveEnemies = (map) => {
  const enemies = enemyPositionsFromMap(map)
  const playerPos = playerPosFromMap(map)

  let paths = []

  enemies.forEach((enemy)=> {
    const path = findPath(map, [enemy.y, enemy.x], [playerPos.y, playerPos.x])
    console.log(path)
    
    if(path.length>0){
      paths.push(path)

      // MOVE ENEMY HARDCODED
      const [enemyNextPosY, enemyNextPostX] = path[1]
      map[enemyNextPosY][enemyNextPostX] = 6
      map[enemy.y][enemy.x] = 0
    }
  })

  pathWays = paths
}

document.addEventListener('keydown', function checkKey(e) {
  let move = null
  if(event.keyCode === 37) move = {x: -1} // left
  if(event.keyCode === 39) move = {x: 1}  // right
  if(event.keyCode === 40) move = {y: 1}  // down
  if(event.keyCode === 38) move = {y: -1} // up
  
  if(!move) return

  tryMovePlayer(currentMap, move, function playerMoved(currentCellId, targetCellId) {
      
      moveEnemies(currentMap)
    
      if(targetCellId === PORTAL){ // change map, on portal
        setTimeout(function(){ 
          mapIndex += 1
          currentMap = maps[mapIndex]
        }, 500);
      }
  })
})

function step(timestamp) {
  elapsedTime = timestamp
  
  // if(elapsedTime >= 30000.0){
  //   elapsedTime = 0
  // }
  
  if (!startTime) startTime = timestamp;
  var dt = timestamp - startTime;

  renderGame(c, currentMap, dt, elapsedTime, pathWays, currentScore)
  
  startTime = timestamp
  window.requestAnimationFrame(step)
}

window.requestAnimationFrame(step)

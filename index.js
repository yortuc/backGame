import { 
  CELL_SIZE, 
  ENEMY_CELLS, 
  PLAYER_CONTAINER_CELLS, 
  PORTAL 
} from './constants.js'

import { map1, map2 } from './maps.js'
import { clearScreen, drawSpiral } from './graphics.js'
import { tryMovePlayer } from './player.js'
import { findPath } from './pathFinding.js'

const c = document.getElementById("c").getContext("2d")

const maps = [map1, map2]

let mapIndex = 0
let currentMap = maps[0]

let startTime = null
let elapsedTime = 0

let score = {
  health: 100,
  moves: 0,
  enemiesAlive: 2,
  keysCollected: 0
}

let pathWays = [[]]

const renderGame = (m, dt) => {
  c.save()
//   console.log(dt)
  clearScreen(c)
  c.translate(0.5, 0.5)
  
  for(let j=0; j<m.length; j++){
    for(let i=0; i<m.length; i++){
      renderCell(j, i, m[j][i])
    }
  }

  drawPathways(pathWays)

  c.font = '16px serif'
  c.fillText("Health: 100%", 500, 50)

  c.restore()
}

const renderHud = (score) => {
  c.fillColor = "red"
  c.font = '20px serif'
  c.fillText("Health: 100 %", 0, 0)
}

const createTileRect = (j,i) => [i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE]

const drawEmptyCell = (j, i) => {
  c.fillStyle = "white"
  const rct = createTileRect(j, i)
  c.fillRect(...rct)
  c.strokeRect(...rct)
}

const drawWall = (j, i) => {
  c.fillStyle = "black"
  c.fillRect(...createTileRect(j, i))
}

const drawPlayer = (j, i) => {
  c.fillStyle = 'red'
  c.beginPath();
  c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, CELL_SIZE/2.5, 0, 2 * Math.PI);
  c.fill();
}

const drawAnt = (j, i) => {
  const index = Math.floor(elapsedTime / 100)
  //   console.log(index)
  const colors = ["orange"]
  
  c.fillStyle = 'black'
  c.beginPath();
  c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, CELL_SIZE/6, 0, 2 * Math.PI);
  c.fill();

  c.moveTo(i*CELL_SIZE, j*CELL_SIZE + CELL_SIZE/2)
  c.lineTo(i*CELL_SIZE + CELL_SIZE, j*CELL_SIZE + CELL_SIZE/2)
  c.stroke()
  
  c.moveTo(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE)
  c.lineTo(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE)
  c.stroke()
}

const drawPortal = (j, i) => {
  const index = Math.floor(elapsedTime / 100)
//   console.log(index)
  const colors = ["orange"]  
  c.strokeStyle = "orange"
  drawSpiral(c, j, i, 0, -index)
}

const renderCell = (j, i, id) => {
  c.save()
  switch(id) {
    case 0:
      drawEmptyCell(j, i)
      break
   case 1:
      drawWall(j, i)
      break
   case 2:
     drawEmptyCell(j, i)
     drawPlayer(j, i)
     break
  case 3:
     drawEmptyCell(j, i)
     drawPortal(j, i)
     break
  case 5:
     drawEmptyCell(j, i)     
     drawPlayer(j, i)
     drawPortal(j, i)
     break
  case 6:
      drawEmptyCell(j,i)
      drawAnt(j, i)
  }
  c.restore()
}

const drawPathways = (paths) => {
  const colors = ["red", "blue", "green", "orange"]

  paths.forEach((path, index) => {
    c.save()
    c.strokeStyle = colors[index % colors.length]
    for(let i=0; i<path.length-1; i++){
      let [y1, x1] = path[i]
      let [y2, x2] = path[i+1]

      c.moveTo(x1 * CELL_SIZE + CELL_SIZE/2, y1 * CELL_SIZE + CELL_SIZE/2)
      c.lineTo(x2 * CELL_SIZE + CELL_SIZE/2, y2 * CELL_SIZE + CELL_SIZE/2)
      c.stroke()
    }
    c.restore()
  })
}
 
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

      const [_y, _x] = path[1]
      map[_y][_x] = 6
      map[enemy.y][enemy.x] = 0  
    }
  })

  pathWays = paths
}

document.addEventListener('keydown', function checkKey(e) {
  let move
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
  
  if(elapsedTime >= 30000.0){
    elapsedTime = 0
  }
  
  if (!startTime) startTime = timestamp;
  var dt = timestamp - startTime;

  renderGame(currentMap, dt, timestamp)
  
  startTime = timestamp
  window.requestAnimationFrame(step)
}

window.requestAnimationFrame(step)




const CELL_SIZE = 40
const GAME_WIDTH = 480
const GAME_HEIGHT = 320

const c = document.getElementById("c").getContext("2d")

// 0: empty cell
// 1: wall
// 2: empty cell with player on it
// 3: portal
// 4: no-func cell for now
// 5: portal with player on it
// 6: ant
const PLAYER_MOVABLE_CELLS = [
  0, 3
]
const PLAYER_CONTAINER_CELLS = [
  2, 5
]

// cell transitions
const PLAYER_MOVE_CELL_TRANSITIONS = {
  2 : 0, // empty cell with player -> empty player
  0 : 2, // empty cell -> empty cell with player on it
  3 : 5, // portal -> portal with player on it
  5 : 3  // portal with player -> portal
}

const map1 = [
  [0, 3, 0, 4],
  [0, 0, 0, 0],
  [0, 0, 1, 6],
  [2, 0, 0, 0]
]

const map2 = [
  [4, 2, 1, 4],
  [0, 0, 1, 4],
  [0, 1, 4, 4],
  [0, 3, 4, 4]  
]

const maps = [map1, map2]

let mapIndex = 0
let currentMap = maps[0]

let startTime = null
let elapsedTime = 0

const clearScreen = () => {
  c.fillStyle = 'rgba(255, 255, 255, 0.2)'
  c.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT)
}

const renderGame = (m, dt) => {
  c.save()
//   console.log(dt)
  clearScreen()
  c.translate(0.5, 0.5)
  
  for(let j=0; j<m.length; j++){
    for(let i=0; i<m.length; i++){
      renderCell(j, i, m[j][i])
    }
  }
  c.restore()
}

const drawEmptyCell = (j, i) => {
  c.fillStyle = "white"
  const rct = [i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE]
  c.fillRect(...rct)
  c.strokeRect(...rct)
}

const drawWall = (j, i) => {
  c.fillStyle = "black"
  c.fillRect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
}

const drawPlayer = (j, i) => {
  c.fillStyle = 'red'
  c.beginPath();
  c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, CELL_SIZE/2.5, 0, 2 * Math.PI);
  c.fill();
}

const drawAnt = (j, i) => {
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

const drawCircle = (j, i, r=9) => {
  c.beginPath();
  c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, r, 0, 2 * Math.PI)
  c.stroke();
}

const drawSpiral = (j, i, radius, angle) => {
  c.beginPath()
  c.moveTo(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2)

  for (var n = 0; n < 150; n++) {
        radius += 0.08;
        // make a complete circle every 50 iterations
        angle += (Math.PI * 2) / 50
        var x = i * CELL_SIZE + CELL_SIZE/2 + radius * Math.cos(angle)
        var y = j * CELL_SIZE + CELL_SIZE/2 + radius * Math.sin(angle)
        c.lineTo(x, y)
   }
    
   c.stroke()
}

const drawPortal = (j, i) => {
  const index = Math.floor(elapsedTime / 100)
//   console.log(index)
  const colors = ["orange"]  
  c.strokeStyle = "orange"
  drawSpiral(j, i, 0, -index)
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
     drawPortal(j, i)
     drawPlayer(j, i)
     break
  case 6:
      drawEmptyCell(j,i)
      drawAnt(j, i)
  }
  c.restore()
}

const getPlayerPosFromMap = (map) => {
  for(let j=0; j<map.length; j++){
    for(let i=0; i<map.length; i++){
      const cellId = map[j][i]
      if(PLAYER_CONTAINER_CELLS.includes(cellId)) {
        return {x: i, y:j, id: cellId}
      }
    }
  }
}

const tryMovePlayer = (map, move, playerMovedCallback) => {
  const {x, y} = getPlayerPosFromMap(map)
  
  if(move.x){
      _x = x + move.x
      if(_x >= 0 && _x < map[0].length && PLAYER_MOVABLE_CELLS.includes(map[y][_x])){
        const currentCellId = map[y][x]
        const targetCellId = map[y][_x]
        map[y][_x] = PLAYER_MOVE_CELL_TRANSITIONS[targetCellId]
        map[y][x] = PLAYER_MOVE_CELL_TRANSITIONS[currentCellId]
        playerMovedCallback(currentCellId, targetCellId)
      }
  }
  
  if(move.y){
      _y = y + move.y
      if(_y >= 0 && _y < map.length && PLAYER_MOVABLE_CELLS.includes(map[_y][x])){
        const currentCellId = map[y][x]
        const targetCellId = map[_y][x]
        map[_y][x] = PLAYER_MOVE_CELL_TRANSITIONS[targetCellId]
        map[y][x] = PLAYER_MOVE_CELL_TRANSITIONS[currentCellId]
        playerMovedCallback(currentCellId, targetCellId)
      }
  }
}


document.addEventListener('keydown', function checkKey(e) {
  let move
  if(event.keyCode === 37) move = {x: -1} // left
  if(event.keyCode === 39) move = {x: 1}  // right
  if(event.keyCode === 40) move = {y: 1}  // down
  if(event.keyCode === 38) move = {y: -1} // up
  
  tryMovePlayer(currentMap, move, function playerMoved(currentCellId, targetCellId) {
      if(targetCellId === 3){ // change map, on portal
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




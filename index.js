import { CELL_SIZE } from './constants.js'

import { map1, map2 } from './maps.js'

import { clearScreen, drawCircle, drawSpiral } from './graphics.js'

import { tryMovePlayer } from './player.js'

const c = document.getElementById("c").getContext("2d")

const maps = [map1, map2]

let mapIndex = 0
let currentMap = maps[0]

let startTime = null
let elapsedTime = 0

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
     drawPortal(j, i)
     drawPlayer(j, i)
     break
  case 6:
      drawEmptyCell(j,i)
      drawAnt(j, i)
  }
  c.restore()
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




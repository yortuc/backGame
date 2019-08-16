import {CELL_SIZE} from './constants.js'
import {drawSpiral} from './graphics.js'

const drawEmptyCell = (c, j, i) => {
  c.fillStyle = "white"
  const rct = [i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE]
  c.fillRect(...rct)
  c.strokeRect(...rct)
}

const drawWall = (c, j, i) => {
  c.fillStyle = "black"
  c.fillRect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
}

const drawPlayer = (c, j, i) => {
  c.fillStyle = 'red'
  c.beginPath();
  c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, CELL_SIZE/2.5, 0, 2 * Math.PI);
  c.fill();
}

const drawAnt = (c, j, i) => {
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

const drawPortal = (c, elapsedTime, j, i) => {
  const index = Math.floor(elapsedTime / 100)
//   console.log(index)
  const colors = ["orange"]  
  c.strokeStyle = "orange"
  drawSpiral(c, j, i, 0, -index)
}

export const renderCell = (c, elapsedTime, j, i, id) => {
  c.save()
  switch(id) {
    case 0:
      drawEmptyCell(c, j, i)
      break
   case 1:
      drawWall(c, j, i)
      break
   case 2:
     drawEmptyCell(c, j, i)
     drawPlayer(c, j, i)
     break
  case 3:
     drawEmptyCell(c, j, i)
     drawPortal(c, elapsedTime, j, i)
     break
  case 5:
     drawEmptyCell(c, j, i)
     drawPlayer(c, j, i)
     drawPortal(c, elapsedTime, j, i)
     break
  case 6:
      drawEmptyCell(c, j,i)
      drawAnt(c, j, i)
  }
  c.restore()
}
import { CELL_SIZE } from './constants.js'
import { clearScreen, drawSpiral } from './graphics.js'

export const renderGame = (c, m, dt, elapsedTime, pathWays, score) => {
  c.save()
//   console.log(dt)
  clearScreen(c)
  c.translate(0.5, 0.5)
  
  for(let j=0; j<m.length; j++){
    for(let i=0; i<m.length; i++){
      renderCell(c, j, i, m[j][i], elapsedTime)
    }
  }

  drawPathways(c, pathWays)
  drawHud(c, score)

  c.restore()
}

const drawHud = (c, score) => {
    c.save()
    c.fillColor = "red"
    c.font = '20px serif'
    c.fillText("Health: 100 %", 0, 0)
    c.restore()
}

const createTileRect = (j,i) => [i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE]

const drawEmptyCell = (c, j, i) => {
  c.fillStyle = "white"
  const rct = createTileRect(j, i)
  c.fillRect(...rct)
  c.strokeRect(...rct)
}

const drawWall = (c, j, i) => {
  c.fillStyle = "black"
  c.fillRect(...createTileRect(j, i))
}

const drawPlayer = (c, j, i) => {
  c.fillStyle = 'red'
  c.beginPath();
  c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, CELL_SIZE/2.5, 0, 2 * Math.PI);
  c.fill();
}

const drawAnt = (c, j, i, elapsedTime) => {
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

const drawPortal = (c, j, i, elapsedTime) => {
  const index = Math.floor(elapsedTime / 100)
//   console.log(index)
  const colors = ["orange"]  
  c.strokeStyle = "orange"
  drawSpiral(c, j, i, 0, -index)
}

const renderCell = (c, j, i, id, elapsedTime) => {
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
     drawPortal(c, j, i, elapsedTime)
     break
  case 5:
     drawEmptyCell(c, j, i)     
     drawPlayer(c, j, i)
     drawPortal(c, j, i, elapsedTime)
     break
  case 6:
      drawEmptyCell(c, j,i)
      drawAnt(c, j, i, elapsedTime)
  }
  c.restore()
}

const drawPathways = (c, paths) => {
  const colors = ["red", "blue", "green", "orange"]

  paths.forEach((path, index) => {
    c.save()
    c.strokeStyle = colors[index % colors.length]
    
    for(let i=1; i<path.length-1; i++){
      let [y1, x1] = path[i]
      let [y2, x2] = path[i+1]

      c.moveTo(x1 * CELL_SIZE + CELL_SIZE/2, y1 * CELL_SIZE + CELL_SIZE/2)
      c.lineTo(x2 * CELL_SIZE + CELL_SIZE/2, y2 * CELL_SIZE + CELL_SIZE/2)
      c.stroke()
    }
    c.restore()
  })
}
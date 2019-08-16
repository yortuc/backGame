import { CELL_SIZE } from './constants.js'

import { renderGame } from './mapRenderer.js'
//   import { tryMovePlayer } from './player.js'
//   import { findPath } from './pathFinding.js'
  
const canvas = document.getElementById("c")
const p = document.getElementById("p")
const c = canvas.getContext("2d")

let currentMap = [
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
]
let startTime = null
let elapsedTime = 0
let pathWays = [[]]

let currentCellType = 0
  
function step(timestamp) {
    elapsedTime = timestamp

    if (!startTime) startTime = timestamp;
    var dt = timestamp - startTime;

    renderGame(c, currentMap, dt, elapsedTime, pathWays)

    startTime = timestamp
    window.requestAnimationFrame(step)
}
  
window.requestAnimationFrame(step)
  
document.addEventListener('keydown', function checkKey(e) {
    const code = e.keyCode
    if(code === 53 || code < 48 || code > 57) return
    
    currentCellType = e.keyCode - 48
    console.log(currentCellType)

    for (let item of document.getElementsByTagName("button")) {
        item.classList.remove("selected")
    }
    document.getElementById("b" + currentCellType.toString()).classList.add("selected")
})

canvas.addEventListener('click', function(e) {
    const pos = getPosition(e)

    const x = Math.floor(pos.x / CELL_SIZE)
    const y = Math.floor(pos.y / CELL_SIZE)

    console.log("CELL:", y, x)

    updateMap(y, x, currentCellType)
})

const getPosition = (event) => {
    let x = event.x
    let y = event.y
    x -= canvas.offsetLeft
    y -= canvas.offsetTop
    return {x, y}
}

const updateMap = (y, x, val) => {
    currentMap[y][x] = val
    p.innerHTML = mapToHtml(currentMap)
}

const mapToHtml= (map) => {
    let ret = ""
    for(let j=0; j<map.length; j++){
        let row = ""
        for(let i=0; i<map.length; i++){
            row = row + "," + map[j][i]
        }
        ret = ret + "</br>" + row
    }
    return ret
}
import { CELL_SIZE, GAME_HEIGHT, GAME_WIDTH, COLORS } from './constants.js'

export const clearScreen = (c) => {
    c.save()
    c.fillStyle = 'rgba(255, 255, 255, 0.2)'
    c.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT)
    c.restore()
}

export const drawCircle = (c, j, i, r=9) => {
    c.beginPath()
    c.arc(i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE + CELL_SIZE/2, r, 0, 2 * Math.PI)
    c.stroke()
}

export const drawSpiral = (c, j, i, radius, angle) => {
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

export const drawSprite = (c, j, i, sprite) => {
    const width = CELL_SIZE / (sprite[0].length)
    c.save()  
    for(let y = 0; y<sprite.length; y++){
        for(let x = 0; x<sprite[0].length; x++){
            c.fillStyle = COLORS[sprite[y][x]]
            c.fillRect(i*CELL_SIZE + x*width, j*CELL_SIZE + y*width, width, width)
        }
    }
    c.restore()
}

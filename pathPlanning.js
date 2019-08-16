import { PLAYER_MOVABLE_CELLS } from "./constants.js";

const ENEMY_MOVABLE_CELLS = PLAYER_MOVABLE_CELLS.concat([2])

export const shortestPath = (map, sourcePoint, targetPoint) => {
    
    let shortestPath = null

    const stepMove = (map, path, candidatePoint, targetPoint) => {

        if(candidatePoint.x === targetPoint.x && 
           candidatePoint.y === targetPoint.y){
            // found the target
            if(!shortestPath || (shortestPath && path.length < shortestPath.length)){
                shortestPath = path
            }
        }
        else{
            const getCell = (j, i) => {
                if(j>=0 && j<map.length && 
                   i>=0 && i<map[0].length &&
                   ENEMY_MOVABLE_CELLS.includes(map[j][i]) &&
                   path.filter(p => p.x === i && p.y === j).length === 0){
                       return {x:i, y:j}
                   }
                else{ return null }
            }
    
            // get movable neighbors
            const {x, y} = candidatePoint
            let neighbors = [               getCell(y-1, x),
                                getCell(y, x-1),               getCell(y, x+1),
                                               getCell(y+1, x)]
            neighbors.forEach(n => {
                if(n){
                    stepMove(map, [...path, n], n, targetPoint)
                }
            })
        }
    }

    stepMove(map, [sourcePoint], sourcePoint, targetPoint)
    
    return shortestPath
}
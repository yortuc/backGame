import time

from constants import PlayerAction
from map_utilities import clear_console_output, print_map
from Level import Level
from WYB import WatchYourBack

level_data2 = [
    [6,0,0,0,3,0,0,6],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0]
]

moves = [[0, -1], [0, -1], [0, -1], [0, 1], [0, -1], [0, -1], [1, 0], [0, -1], [0, -1], [0, -1]]

game = WatchYourBack(Level(level_data2))

for move in moves:
    clear_console_output()
    game.move_player(PlayerAction(move))
    game.move_enemies()
    print_map(game.level.level)
    time.sleep(1)

print('finished')
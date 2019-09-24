import time

import numpy as np
from constants import LEVEL2, ACTIONS, GameStatus
from Level import Level
from WYB import WatchYourBack
from map_utilities import clear_console_output, encode_map_numeric, print_map
from dql import DQNAgent

game = WatchYourBack(Level(LEVEL2))
state_size = len(LEVEL2)**2
agent = DQNAgent(state_size, 4)
agent.epsilon = 0
agent.load("./save/level2.h5")

clear_console_output()
print_map(game.level.level)
time.sleep(2)

while game.status == GameStatus.ONGOING:
    state = encode_map_numeric(game.level.level)
    player_move = agent.act(np.reshape(state, [1, state_size]))

    game.move_player(ACTIONS[player_move])
    clear_console_output()
    print_map(game.level.level)
    time.sleep(2)

    game.move_enemies()
    clear_console_output()
    print_map(game.level.level)
    time.sleep(2)

print('Result:', game.status)
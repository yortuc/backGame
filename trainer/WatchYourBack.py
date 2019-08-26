############ WatchYourBack Environment ############
# 
# expose same api with gym 
# so I dont need to change the training code
# 
###################################################

import random

from copy import copy, deepcopy
from map_utilities import encode_map, print_map
from constants import PLAYER_ON_EMPTY_CELL, PLAYER_ON_PORTAL, PORTAL, EMPTY_CELL, PLAYER_CONTAINER_CELLS, PLAYER_MOVABLE_CELLS

class Space:
    def __init__(self, n):
        self.n = n
    def sample(self):
        return random.randint(0, self.n-1)

class WatchYourBack:
    def __init__(self, original_map, states):
        self.states = states
        self.original_map = original_map
        self.map = None
        self.action_space = Space(4)
        self.observation_space = Space(len(states))
        self.action_mapping = {
            0: [0, -1],
            1: [1,  0],
            2: [0,  1],
            3: [-1, 0]
        }
        self.reset()
    
    def reset(self):
        self.map = deepcopy(self.original_map)
        return self.states[encode_map(self.map)]
        
    def get_player_pos(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[0])):
                if self.map[j][i] in PLAYER_CONTAINER_CELLS:
                    return [j, i]

    def render(self):
        print_map(self.map)
                
    def close(self):
        return 0
    
    def move_entity(self, position, action, goal_cell_id, movable_cells, cell_id, after_goal_cell_id):
        done = False
        new_state = None
        reward = 0
        info = None

        [delta_x, delta_y] = self.action_mapping[action]
        [pos_y, pos_x] = position
        [target_y, target_x] = [pos_y + delta_y, pos_x + delta_x]

        # if entity can move
        if target_x >= 0 and target_x < len(self.map[0]) and \
            target_y >= 0 and target_y < len(self.map) and \
            self.map[target_y][target_x] in movable_cells:

            targetCellId = self.map[target_y][target_x]
            self.map[pos_y][pos_x] = 0

            if targetCellId == goal_cell_id:
                # hit the goal
                reward = 1
                done = True
                self.map[target_y][target_x] = after_goal_cell_id
                info = "hit the goal!"
            else:
                self.map[target_y][target_x] = cell_id
                info = f"player moved to {target_y} {target_x}"
        else:
            info = "player could not move"
            
        new_state = self.states[encode_map(self.map)]
        return new_state, reward, done, info

    def step(self, action):
        # new_state, reward, done, info = env.step(action)
        #
        # 0: up, 1: right, 2: down, 3: left
        
        done = False

        player_pos = self.get_player_pos()
        state_after_player_move, reward, done, info = self.move_entity(
            position = player_pos, 
            action = action, 
            goal_cell_id = PORTAL,
            movable_cells = PLAYER_MOVABLE_CELLS,
            cell_id = PLAYER_ON_EMPTY_CELL,
            after_goal_cell_id = PLAYER_ON_PORTAL
        )
        
        return state_after_player_move, reward, done, info
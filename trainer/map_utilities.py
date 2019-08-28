from copy import copy, deepcopy
from constants import EMPTY_CELL

def encode_map(m):
    ret = ''
    for r in m:
        ret = ret + ''.join([str(c) for c in r])
    return ret

def decode_map(s, size):
    ret = []
    for j in range(size):
        row = []
        for i in range(size):
            row.append(s[j*size + i])
        ret.append(row)
    return ret

def print_map(m):
    for row in m:
        print(row)

def create_states_for_playerless_map(m, enemy_count=0):
    # player movements
    states = []
    for j in range(len(m)):
        for i in range(len(m[0])):
            if m[j][i] == 0:
                copy_m = deepcopy(m)
                copy_m[j][i] = 2 # move player to there
                states.append(encode_map(copy_m))
        
    # enemies 
    states_with_enemy = []    
    for s in states:
        for cellIndex in range(len(s)):
            cell = int(s[cellIndex])
            if cell == EMPTY_CELL:
                copy_s = s[:cellIndex] + '6' + s[cellIndex+1:]
                states_with_enemy.append(copy_s)

    # player reaching the goal
    states_with_goal = states_with_enemy[:]
    for s in states_with_enemy:
        for cellIndex in range(len(s)):
            cell = int(s[cellIndex])
            if cell == 3:
                copy_s = s[:cellIndex] + '5' + s[cellIndex+1:]
                copy_s = copy_s.replace('2', '0')
                states_with_goal.append(copy_s)

    # enemy eating player
    states_with_enemy_reaching_goal = states_with_goal[:]
    for s in states_with_enemy_reaching_goal:
        for cellIndex in range(len(s)):
            cell = int(s[cellIndex])
            if cell == 2:
                copy_s = s[:cellIndex] + '0' + s[cellIndex+1:]
                states_with_enemy_reaching_goal.append(copy_s)

    # convert to state dictionary
    states_with_goal_unq = list(set(states_with_enemy_reaching_goal))
    dct = {}
    for index in range(len(states_with_goal_unq)):
        dct[states_with_goal_unq[index]] = index
    return dct
    
import networkx as nx
from copy import copy, deepcopy
from constants import WALL, EMPTY_CELL, PLAYER_MOVABLE_CELLS, ENEMY_ANT, PLAYER_ON_EMPTY_CELL

def encode_map(m):
    ret = ''
    for r in m:
        ret = ret + ''.join([str(c) for c in r])
    return ret

def encode_map_numeric(m):
    return [float(k)/7.0 for k in encode_map(m)]

def decode_map(s, size):
    ret = []
    for j in range(size):
        row = []
        for i in range(size):
            row.append(s[j*size + i])
        ret.append(row)
    return ret

def print_map(m):
    pm = {
        0: '⬜️',
        6: '🕷',
        2: '●',
        5: 'o',
        3: '🏵',
        1: '🔳'
    }
    for row in m:
        rww =''.join([pm[t] for t in row])
        print(rww)

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
    

def clear_console_output():
    import os
    clear = lambda: os.system('clear')
    clear()

def map_to_graph(m):
    G = nx.grid_2d_graph(len(m), len(m), periodic=False, create_using=None)

    for j in range(len(m)):
        for i in range(len(m[j])):
            cell = m[j][i]
            # if cell not in PLAYER_MOVABLE_CELLS + [ENEMY_ANT, PLAYER_ON_EMPTY_CELL]:
            if cell == WALL:
                G.remove_node((j, i))
    return G

def euclidean_distance(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def get_shortest_path(graph, source, target):
    source_tuple = (source[0], source[1])
    target_tuple = (target[0], target[1])
    return nx.astar_path(graph, source_tuple, target_tuple, euclidean_distance)

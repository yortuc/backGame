from copy import copy, deepcopy

from constants import PLAYER_ON_EMPTY_CELL, PLAYER_ON_PORTAL, \
PORTAL, EMPTY_CELL, ENEMY_ANT, PLAYER_CONTAINER_CELLS, PLAYER_MOVABLE_CELLS, ENEMY_MOVABLE_CELLS
from map_utilities import map_to_graph

class Level:
    def __init__(self, level):
        self.level = level
        self.height = len(level)
        self.width = len(level[0])
        self.graph = map_to_graph(self.level)

    def update_graph(self):
        self.graph = map_to_graph(self.level)

    def get_portal_pos(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.level[j][i] == PORTAL:
                    return [j, i]

    def get_player_pos(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.level[j][i] in PLAYER_CONTAINER_CELLS:
                    return [j, i]

    def get_enemy_positions(self):
        ret = []
        for j in range(self.height):
            for i in range(self.width):
                if self.level[j][i] == ENEMY_ANT:
                    ret.append([j, i])
        return ret
    
    def get_cell(self, y, x):
        return self.level[y][x]

    def set_cell(self, y, x, cell_value):
        self.level[y][x] = cell_value
        self.update_graph()

    def can_player_move_to_pos(self, target_y, target_x):
        return target_x >= 0 and target_x < self.width and \
            target_y >= 0 and target_y < self.height and \
            self.get_cell(target_y, target_x) in PLAYER_MOVABLE_CELLS

    def copy(self):
        return deepcopy(self.level)

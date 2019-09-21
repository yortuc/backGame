import random

from Level import Level
from copy import copy, deepcopy
from map_utilities import encode_map, print_map, get_shortest_path, map_to_graph
from constants import PLAYER_ON_EMPTY_CELL, PLAYER_ON_PORTAL, \
PORTAL, EMPTY_CELL, ENEMY_ANT, PLAYER_CONTAINER_CELLS, PLAYER_MOVABLE_CELLS, ENEMY_MOVABLE_CELLS,\
PlayerAction, GameStatus


class WatchYourBack:
    def __init__(self, level: Level):
        self.level = level
        self.status = GameStatus.ONGOING

    def move_player(self, action: PlayerAction):
        """move player with the given action -> 0,1,2,3
        """
        [delta_x, delta_y] = action.value
        [pos_y, pos_x] = self.level.get_player_pos()
        [target_y, target_x] = [pos_y + delta_y, pos_x + delta_x]

        # if player can move
        if self.level.can_player_move_to_pos(target_y, target_x):
            targetCellId = self.level.get_cell(target_y, target_x)
            self.level.set_cell(pos_y, pos_x, EMPTY_CELL)

            if targetCellId == PORTAL:
                self.level.set_cell(target_y, target_x, PLAYER_ON_PORTAL)
                self.status = GameStatus.PLAYER_WON
            else:
                self.level.set_cell(target_y, target_x, PLAYER_ON_EMPTY_CELL)
            return True
        else:
            return False

    def move_enemies(self):
        """move enemies with shortest path algorithm
        """
        player_pos = self.level.get_player_pos()
        enemy_positions = self.level.get_enemy_positions()

        # print("graph nodes:")
        # print(self.level.graph.nodes)
        # print(self.level.level)

        for enemy_pos in enemy_positions:
            path = get_shortest_path(self.level.graph, enemy_pos, player_pos)

            if len(path) > 0:
                (enemyNextPosY, enemyNextPostX) = path[1]

                # player got eaten?
                if player_pos == [enemyNextPosY, enemyNextPostX]:
                    self.status = GameStatus.PLAYER_LOST

                self.level.set_cell(enemyNextPosY, enemyNextPostX, ENEMY_ANT)
                self.level.set_cell(enemy_pos[0], enemy_pos[1], EMPTY_CELL)

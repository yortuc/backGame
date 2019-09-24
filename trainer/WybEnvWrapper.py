import math
from copy import copy, deepcopy
from map_utilities import encode_map_numeric

from constants import ACTIONS, GameStatus
from Level import Level
from WYB import WatchYourBack

class WybEnv:
    def __init__(self, level_data):
        self.observation_space = 1000
        self.original_level_data = deepcopy(level_data)
        self.game = WatchYourBack(Level(deepcopy(self.original_level_data)))
        self.last_pos = self.game.level.get_player_pos()

    def get_observation_space(self):
        return len(encode_map_numeric(self.original_level_data))

    def reset(self):
        # reset env return initial state
        self.game = WatchYourBack(Level(deepcopy(self.original_level_data)))
        self.last_pos = self.game.level.get_player_pos()
        return encode_map_numeric(self.game.level.level)

    def step(self, action):
        # next_state, reward, done, _ = env.step(action)
        # print("taking action", action, self.game.status, self.game.level.level)
        self.last_pos = self.game.level.get_player_pos()
        player_action = ACTIONS[action]
        did_player_move = self.game.move_player(player_action)
        done = False
        reward = 0

        if did_player_move:
            if self.game.status == GameStatus.PLAYER_WON:
                reward = 100000
                done = True
            else:
                self.game.move_enemies()

                if self.game.status == GameStatus.PLAYER_LOST:
                    reward = -10000
                    done = True
                elif self.game.status == GameStatus.ONGOING:
                    # player_pos = self.last_pos
                    # portal_pos = self.game.level.get_portal_pos()
                    # distance_to_portal = math.sqrt((player_pos[1] - portal_pos[1])**2 + (player_pos[0] - portal_pos[0])**2)
                    # reward = 1000.0/distance_to_portal
                    reward = 0
        else:
            reward = -1000

        return encode_map_numeric(self.game.level.level), reward, done, self.game.status.name
        

    
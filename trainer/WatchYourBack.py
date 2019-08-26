############ WatchYourBack Environment ############
# 
# expose same api with gym 
# so I dont need to change the training code
# 
###################################################

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
    
    def move_enemies(self):
        [player_pos_y, player_pos_x] = self.get_player_pos()
    
    def step(self, action):
        # new_state, reward, done, info = env.step(action)
        #
        # 0: up, 1: right, 2: down, 3: left
        
        done = False
        new_state = None
        reward = 0
        info = None
        
        xy = {
            0: [0, -1],
            1: [1,  0],
            2: [0,  1],
            3: [-1, 0]
        }
        
        [delta_x, delta_y] = xy[action]
        [player_pos_y, player_pos_x] = self.get_player_pos()
        [target_pos_y, target_pos_x] = [player_pos_y + delta_y, player_pos_x + delta_x]
        
        if target_pos_x >= 0 and target_pos_x < len(self.map[0]) and \
            target_pos_y >= 0 and target_pos_y < len(self.map) and \
            self.map[target_pos_y][target_pos_x] in PLAYER_MOVABLE_CELLS:

            targetCellId = self.map[target_pos_y][target_pos_x]
            self.map[player_pos_y][player_pos_x] = 0

            if targetCellId == 3:
                # hit the goal
                reward = 1
                done = True
                self.map[target_pos_y][target_pos_x] = 5
                info = "hit the goal!"
            else:
                self.map[target_pos_y][target_pos_x] = 2
                info = f"player moved to {target_pos_y} {target_pos_x}"
        
        else:
            info = "player could not move"
            
        # each state has a number value
        new_state = self.states[encode_map(self.map)]
        
        return new_state, reward, done, info
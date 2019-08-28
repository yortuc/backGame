import numpy as np
import time
import random

from IPython.display import clear_output
from map_utilities import create_states_for_playerless_map
from WatchYourBack import WatchYourBack


states = create_states_for_playerless_map([
    [1, 0, 3],
    [0, 0, 0],
    [0, 0, 0]
], enemy_count = 1)

print('states', states)

original_map = [
    [1, 0, 3],
    [6, 0, 0],
    [0, 0, 2]
]

env = WatchYourBack(original_map, states)

########################################
# Initialize q-table                   #
#                                      #
# rows: state space in the environment #
# columns: action space.               #
########################################

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table_player = np.zeros((state_space_size, action_space_size))
q_table_enemy = np.zeros((state_space_size, action_space_size))

####################################### 
# Setup Hyper parameters              #
#######################################
num_episodes = 100000
max_steps_per_episode = 1000

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

####################################### 
# TRAIN                               #
# Q-learning algorithm                #
#######################################
rewards_all_episodes = []
for episode in range(num_episodes):
    # initialize new episode params
    state = env.reset()
    done = False
    rewards_current_episode = 0
    
    for step in range(max_steps_per_episode): 
        # Exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0, 1)
        
        ##########################
        # PLAYER TRAIN           #
        ##########################
        if random.uniform(0, 1) > exploration_rate:
            player_action = np.argmax(q_table_player[state,:])  # exploit: get highest q-value move
        else:
            player_action = env.action_space.sample()    # explore: select a random move
        
        # Take new player action
        new_state, reward_player, player_done, info = env.step(player_action, 1)

        print(new_state, reward_player, player_done, info)
        
        # Update Q-table
        q_table_player[state, player_action] = q_table_player[state, player_action] * (1 - learning_rate) + \
            learning_rate * (reward_player + discount_rate * np.max(q_table_player[new_state, :]))
        
        if player_done == True: 
            break

        ##########################
        # ENEMY TRAIN            #
        ##########################
        if random.uniform(0, 1) > exploration_rate:
            action_enemy = np.argmax(q_table_enemy[new_state,:])  # exploit: get highest q-value move
        else:
            action_enemy = env.action_space.sample()    # explore: select a random move
        
        # Take new enemy action
        new_state2, reward_enemy, enemy_done, info = env.step(action_enemy, 2)

        print(new_state2, reward_enemy, enemy_done, info)
        
        # Update Q-table
        q_table_enemy[new_state, action_enemy] = q_table_enemy[new_state, action_enemy] * (1 - learning_rate) + \
            learning_rate * (reward_enemy + discount_rate * np.max(q_table_enemy[new_state2, :]))

        # Set new state
        state = new_state2

        # Add new reward        
        rewards_current_episode += reward_player

        if enemy_done == True: 
            break

    # Exploration rate decay   
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    
    # Add current episode reward to total rewards list
    rewards_all_episodes.append(rewards_current_episode)


# Calculate and print the average reward per thousand episodes
rewards_per_thosand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
count = 1000

print("********Average reward per thousand episodes********\n")
for r in rewards_per_thosand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

########################################################
# WATCH IT PLAY!                                       #
# Watch our agent play by playing the best action      #
# from each state according to the Q-table             #
########################################################
for episode in range(3):
    # initialize new episode params
    state = env.reset()
    done = False
    print("*****EPISODE ", episode+1, "*****\n\n\n\n")
    time.sleep(1)

    for step in range(max_steps_per_episode):        
        # Show current state of environment on screen
        clear_output(wait=True)
        env.render()
        time.sleep(0.3)
    
        # Player: Choose action with highest Q-value for current state       
        player_action = np.argmax(q_table_player[state,:])
        new_state, reward, done, info = env.step(player_action, 1)

        if done:
            if reward == 1:
                # Agent reached the goal and won episode
                print("****You reached the goal!****")
                time.sleep(3)
            else:
                # Agent stepped in a hole and lost episode   
                time.sleep(3)
                clear_output(wait=True)
            break
        
        # Player: Choose action with highest Q-value for current state       
        enemy_action = np.argmax(q_table_enemy[new_state,:])
        new_state2, reward2, done2, info2 = env.step(enemy_action, 2)
        
        if done2:
            if reward2 == 1:
                # Agent reached the goal and won episode
                print("****ENEMY WON!****")
                time.sleep(3)
            else:
                # Agent stepped in a hole and lost episode   
                time.sleep(3)
                clear_output(wait=True)
            break

        # Set new state
        state = new_state2
        
env.close()

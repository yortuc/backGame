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

print(states)

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

q_table = np.zeros((state_space_size, action_space_size))

####################################### 
# Setup Hyper parameters              #
#######################################
num_episodes = 10000
max_steps_per_episode = 100

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
        
        # explore or exploit?
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])  # exploit: get highest q-value move
        else:
            action = env.action_space.sample()    # explore: select a random move
        
        # Take new action
        new_state, reward, done, info = env.step(action)

        print(new_state, reward, done, info)
        
        # Update Q-table
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
        
        # Set new state
        state = new_state

        # Add new reward        
        rewards_current_episode += reward 

        if done == True: 
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
    
        # Choose action with highest Q-value for current state       
        action = np.argmax(q_table[state,:])        

        # Take new action
        new_state, reward, done, info = env.step(action)
        
        if done:
            if reward == 1:
                # Agent reached the goal and won episode
                print("****You reached the goal!****")
                time.sleep(3)
            else:
                # Agent stepped in a hole and lost episode   
                time.sleep(3)
                clear_output(wait=True)
            
        # Set new state
        state = new_state
        
env.close()

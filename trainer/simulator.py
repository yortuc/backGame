import time
import numpy as np

from map_utilities import clear_console_output

########################################################
# WATCH IT PLAY!                                       #
# Watch our agent play by playing the best action      #
# from each state according to the Q-table             #
########################################################

def simulate(env,q_table_player, q_table_enemy, max_steps_per_episode, episodes=3):

    for episode in range(episodes):
        # initialize new episode params
        state = env.reset()
        done = False
        print("*****EPISODE ", episode+1, "*****\n\n\n\n")
        time.sleep(1)

        for step in range(max_steps_per_episode):        
            # Show current state of environment on screen
            clear_console_output()
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


def play_against_enemy(env,q_table_player, q_table_enemy):
    state = env.reset()
    done = False
    print("game ready: ")

    clear_console_output()
    env.render()
    
    while not done:
        player_action = int(input())
        new_state, reward, done, info = env.step(player_action, 1)

        clear_console_output()
        env.render()

        if done:
            print("**** YOU WON! ****")
            break
            
        # enemy chooses action with highest Q-value for current state
        enemy_action = np.argmax(q_table_enemy[new_state,:])
        new_state2, reward2, done2, info2 = env.step(enemy_action, 2)
        
        clear_console_output()
        env.render()

        if done2:
            print("**** ENEMY WON! ****")
            break

        state = new_state2
            
    env.close()
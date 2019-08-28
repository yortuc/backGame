from map_utilities import create_states_for_playerless_map, encode_map
from WatchYourBack import WatchYourBack

def flatten_map(m):
    return [element for sub in m for element in sub]

def array_equal(a1, a2):
    return all([a == b for a, b in zip(a1, a2)])
    
def test_move_player():
    states = create_states_for_playerless_map([
        [1, 0, 3],
        [0, 0, 0],
        [0, 0, 0]
    ], enemy_count = 1)

    original_map = [
        [1, 0, 3],
        [6, 0, 2],
        [0, 0, 0]
    ]

    env = WatchYourBack(original_map, states)

    action_move_up = 0
    players_turn = 1
    state_after_player_move, player_reward, player_done, player_info = env.step(action_move_up, players_turn)

    expected_state = states[encode_map([
        [1, 0, 5],
        [6, 0, 0],
        [0, 0, 0]
    ])]

    assert expected_state == state_after_player_move and player_reward == 1 and player_done == True

def test_move_enemy_vertical():
    states = create_states_for_playerless_map([
        [1, 0, 3],
        [0, 0, 0],
        [0, 0, 0]
    ], enemy_count = 1)

    original_map = [
        [1, 0, 3],
        [0, 0, 6],
        [2, 0, 0]
    ]

    env = WatchYourBack(original_map, states)

    action_move_up = 0
    enemys_turn = 2
    state_after_enemy_move, enemy_reward, enemy_done, enemy_info = env.step(action_move_up, enemys_turn)

    expected_state = states[encode_map([
        [1, 0, 3],
        [0, 0, 6],
        [2, 0, 0]
    ])]

    assert expected_state == state_after_enemy_move and enemy_reward == 0

def test_move_enemy_horizontal():
    states = create_states_for_playerless_map([
        [1, 0, 3],
        [0, 0, 0],
        [0, 0, 0]
    ], enemy_count = 1)

    original_map = [
        [1, 6, 3],
        [0, 0, 0],
        [2, 0, 0]
    ]

    env = WatchYourBack(original_map, states)

    action_move_right = 1
    enemys_turn = 2
    state_after_enemy_move, enemy_reward, enemy_done, enemy_info = env.step(action_move_right, enemys_turn)

    expected_state = states[encode_map([
        [1, 6, 3],
        [0, 0, 0],
        [2, 0, 0]
    ])]

    assert expected_state == state_after_enemy_move and enemy_reward == 0 and enemy_done == False
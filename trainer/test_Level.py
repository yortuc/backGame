from Level import Level

level_data = [
    [0, 0, 2],
    [0, 6, 1],
    [6, 0, 0]
]

def test_get_player_pos():
    level = Level(level_data)
    player_pos = level.get_player_pos()
    assert player_pos == [0, 2]

def test_get_enemy_positions():
    level = Level(level_data)
    enemy_positions = level.get_enemy_positions()
    assert enemy_positions == [[1, 1], [2, 0]]

def test_can_player_move_to_pos():
    level = Level(level_data)
    assert level.can_player_move_to_pos(0, 1) == True
    assert level.can_player_move_to_pos(1, 2) == False

def test_graph():
    level = Level([
        [1, 0, 3],
        [6, 0, 2],
        [0, 0, 0]
    ])
    assert list(level.graph.nodes) == [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
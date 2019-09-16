from Level import Level
from WYB import WatchYourBack
from constants import PlayerAction, GameStatus, ENEMY_ANT
from Player import Player

def test_create_player_with_random_genes():
    player = Player(5, None, None)
    assert len(player.genes) == 5

    for action in player.genes:
        assert isinstance(action, PlayerAction) == True
 
def test_move_player_without_enemy():
    game = WatchYourBack(Level([
        [0, 0, 3],
        [2, 0, 0],
        [0, 0, 0]
    ]))
    player = Player(
        step_size=3, 
        game=game, 
        genes=[PlayerAction.RIGHT, PlayerAction.RIGHT, PlayerAction.UP]
    )
    for i in range(0, 3):
        assert player.status == GameStatus.ONGOING
        player.move()
    assert player.status == GameStatus.PLAYER_WON

def test_move_player():
    game = WatchYourBack(Level([
        [2, 0, 3],
        [0, 0, 0],
        [6, 0, 0]
    ]))
    player = Player(
        step_size=1, 
        game=game, 
        genes=[PlayerAction.RIGHT]
    )
    player.move()
    assert player.status == GameStatus.ONGOING
    assert game.level.get_cell(1, 0) == ENEMY_ANT

def test_mutate_genes():
    player = Player(5, None, None)
    player.mutate()
    assert len(player.genes) == 5

def test_calculate_fitness():
    # game = WatchYourBack(Level([
    #     [2, 0, 3],
    #     [0, 0, 0],
    #     [6, 0, 0]
    # ]))
    # player = Player(
    #     step_size=1, 
    #     game=game, 
    #     genes=[PlayerAction.RIGHT]
    # )
    # player.move()
    # assert player.status == GameStatus.ONGOING
    # assert game.level.get_cell(1, 0) == ENEMY_ANT
    pass
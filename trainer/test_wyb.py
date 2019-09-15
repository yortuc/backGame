from constants import PlayerAction
from Level import Level
from WYB import WatchYourBack

from constants import PLAYER_ON_EMPTY_CELL, PLAYER_ON_PORTAL, \
PORTAL, EMPTY_CELL, ENEMY_ANT, PLAYER_CONTAINER_CELLS, PLAYER_MOVABLE_CELLS, ENEMY_MOVABLE_CELLS, \
GameStatus

    
def test_move_player():
    wyb = WatchYourBack(Level([
        [1, 0, 3],
        [0, 0, 2],
        [0, 0, 0]
    ]))

    wyb.move_player(PlayerAction.LEFT)
    assert wyb.level.get_cell(1, 1) == PLAYER_ON_EMPTY_CELL

    wyb.move_player(PlayerAction.UP)
    assert wyb.level.get_cell(0, 1) == PLAYER_ON_EMPTY_CELL

    wyb.move_player(PlayerAction.RIGHT)
    assert wyb.level.get_cell(0, 2) == PLAYER_ON_PORTAL
    assert wyb.status == GameStatus.PLAYER_WON

def test_move_enemies():
    wyb = WatchYourBack(Level([
        [1, 0, 3],
        [6, 0, 2],
        [0, 0, 0]
    ]))
    wyb.move_enemies()
    assert wyb.level.get_cell(1, 1) == ENEMY_ANT
    assert wyb.status == GameStatus.ONGOING

    wyb.move_enemies()
    assert wyb.level.get_cell(1, 2) == ENEMY_ANT
    assert wyb.status == GameStatus.PLAYER_LOST

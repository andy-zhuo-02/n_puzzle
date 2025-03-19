import pytest
import numpy as np
from src.core.board import Board
from src.core.game import Game

def test_board_initialization():
    """测试棋盘初始化"""
    board = Board(3)
    assert board.size == 3
    assert board.state.shape == (3, 3)
    assert board.empty_pos == (2, 2)
    assert board.moves == 0

def test_board_valid_moves():
    """测试有效移动"""
    board = Board(3)
    # 初始状态下，空格在(2,2)，可以移动(2,1)和(1,2)的数字
    assert board.is_valid_move(2, 1)
    assert board.is_valid_move(1, 2)
    assert not board.is_valid_move(0, 0)

def test_board_move():
    """测试移动操作"""
    board = Board(3)
    initial_state = board.get_state().copy()
    # 移动(2,1)位置的数字到空格位置
    assert board.move(2, 1)
    assert board.empty_pos == (2, 1)
    assert board.moves == 1
    # 确保状态已更新
    assert not np.array_equal(board.get_state(), initial_state)

def test_board_is_solved():
    """测试解题判定"""
    board = Board(3)
    # 初始状态就是解决状态
    assert board.is_solved()
    # 移动一次后不是解决状态
    board.move(2, 1)
    assert not board.is_solved()

def test_game_initialization():
    """测试游戏初始化"""
    game = Game(3)
    assert not game.is_running
    assert game.get_moves() == 0

def test_game_start():
    """测试游戏开始"""
    game = Game(3)
    game.start_game()
    assert game.is_running
    assert game.start_time is not None

def test_game_move():
    """测试游戏移动"""
    game = Game(3)
    game.start_game()
    state, empty_pos = game.get_board_state()
    row, col = empty_pos
    
    # 尝试移动一个有效位置
    valid_moves = [
        (row-1, col) if row > 0 else (row+1, col),
        (row, col-1) if col > 0 else (row, col+1)
    ]
    
    move_made = False
    for move_row, move_col in valid_moves:
        if 0 <= move_row < 3 and 0 <= move_col < 3:
            assert game.make_move(move_row, move_col)
            move_made = True
            break
    
    assert move_made
    assert game.get_moves() == 1

def test_game_callbacks():
    """测试游戏回调函数"""
    game = Game(3)
    move_called = False
    reset_called = False
    
    def on_move():
        nonlocal move_called
        move_called = True
        
    def on_reset():
        nonlocal reset_called
        reset_called = True
    
    game.register_callback('on_move', on_move)
    game.register_callback('on_reset', on_reset)
    
    game.start_game()
    assert reset_called
    
    # 尝试一个有效移动
    state, empty_pos = game.get_board_state()
    row, col = empty_pos
    if row > 0:
        game.make_move(row-1, col)
    elif col > 0:
        game.make_move(row, col-1)
    
    assert move_called

if __name__ == '__main__':
    pytest.main([__file__]) 
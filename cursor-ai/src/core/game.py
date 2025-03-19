from typing import Optional, Tuple, List, Callable
from .board import Board
import time

class Game:
    """数字华容道游戏核心逻辑类"""
    
    def __init__(self, size: int = 3):
        """
        初始化游戏
        
        Args:
            size: 棋盘大小，默认为3x3
        """
        self.board = Board(size)
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.callbacks = {
            'on_move': [],
            'on_win': [],
            'on_reset': []
        }
        
    def start_game(self) -> None:
        """开始新游戏"""
        self.board.shuffle()
        # 确保生成的棋盘状态是可解的
        while not self.board.is_solvable():
            self.board.shuffle()
        self.start_time = time.time()
        self.is_running = True
        self._notify('on_reset')
        
    def make_move(self, row: int, col: int) -> bool:
        """
        执行移动
        
        Args:
            row: 要移动的数字的行位置
            col: 要移动的数字的列位置
            
        Returns:
            bool: 移动是否成功
        """
        if not self.is_running:
            return False
            
        if self.board.move(row, col):
            self._notify('on_move')
            if self.board.is_solved():
                self.is_running = False
                self.elapsed_time = time.time() - self.start_time
                self._notify('on_win')
            return True
        return False
        
    def get_elapsed_time(self) -> float:
        """获取游戏已经运行的时间"""
        if not self.is_running:
            return self.elapsed_time
        return time.time() - self.start_time
        
    def get_moves(self) -> int:
        """获取移动步数"""
        return self.board.moves
        
    def get_board_state(self) -> Tuple[List[List[int]], Tuple[int, int]]:
        """
        获取当前游戏状态
        
        Returns:
            Tuple[List[List[int]], Tuple[int, int]]: (棋盘状态, 空格位置)
        """
        return self.board.get_state().tolist(), self.board.get_empty_position()
        
    def reset(self) -> None:
        """重置游戏"""
        self.start_game()
        
    def register_callback(self, event: str, callback: Callable) -> None:
        """
        注册事件回调函数
        
        Args:
            event: 事件名称 ('on_move', 'on_win', 'on_reset')
            callback: 回调函数
        """
        if event in self.callbacks:
            self.callbacks[event].append(callback)
            
    def _notify(self, event: str) -> None:
        """
        通知所有注册的回调函数
        
        Args:
            event: 事件名称
        """
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                callback() 
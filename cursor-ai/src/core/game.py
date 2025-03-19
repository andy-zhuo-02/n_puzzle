from typing import Optional, Tuple, List, Callable, Dict, Any
import numpy as np
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
        self.steps = 0
        self.listeners = []  # 事件监听器列表
        self.callbacks = {
            'on_move': [],
            'on_win': [],
            'on_reset': []
        }
        
    def add_listener(self, listener: Callable[[str, Dict[str, Any]], None]):
        """
        添加事件监听器
        
        Args:
            listener: 监听器函数，接收事件类型和参数
        """
        self.listeners.append(listener)
        
    def _notify_listeners(self, event_type: str, **kwargs):
        """
        通知所有监听器
        
        Args:
            event_type: 事件类型
            **kwargs: 事件参数
        """
        for listener in self.listeners:
            listener(event_type, **kwargs)
        
    def new_game(self):
        """开始新游戏"""
        # 重置棋盘状态
        self.board.reset()
        # 重置游戏状态
        self.start_time = time.time()
        self.elapsed_time = 0
        self.is_running = True
        self.steps = 0
        # 通知监听器
        self._notify_listeners("game_start")
        
    def move(self, row: int, col: int) -> bool:
        """
        移动数字
        
        Args:
            row: 行号
            col: 列号
            
        Returns:
            bool: 是否移动成功
        """
        if not self.is_running:
            return False
            
        if self.board.move(row, col):
            self.steps += 1
            self._notify_listeners("move")
            
            try:
                # 检查是否完成游戏
                if self.board.is_solved():
                    self.is_running = False
                    self.elapsed_time = time.time() - self.start_time
                    self._notify_listeners("game_over")
            except Exception as e:
                print(f"检查游戏是否完成时出错：{str(e)}")
            return True
        return False
        
    def get_elapsed_time(self) -> float:
        """获取游戏已经运行的时间"""
        if not self.is_running:
            return self.elapsed_time
        return time.time() - self.start_time
        
    def get_moves(self) -> int:
        """获取移动步数"""
        return self.steps
        
    def get_board_state(self) -> Tuple[List[List[int]], Tuple[int, int]]:
        """
        获取当前游戏状态
        
        Returns:
            Tuple[List[List[int]], Tuple[int, int]]: (棋盘状态, 空格位置)
        """
        return self.board.get_state().tolist(), self.board.get_empty_position()
        
    def reset(self) -> None:
        """重置游戏"""
        # 重置棋盘状态
        self.board.reset()
        # 重置游戏状态
        self.start_time = time.time()
        self.elapsed_time = 0
        self.is_running = True
        self.steps = 0
        # 通知监听器
        self._notify_listeners("game_start")
        
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

    def undo(self) -> bool:
        """
        撤销上一步移动
        
        Returns:
            bool: 是否撤销成功
        """
        if not self.is_running:
            return False
            
        if self.board.undo():
            self.steps -= 1
            self._notify_listeners("undo")
            return True
        return False 
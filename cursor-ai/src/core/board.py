import numpy as np
from typing import Tuple, List, Optional

class Board:
    """数字华容道游戏棋盘类"""
    
    def __init__(self, size: int = 3):
        """
        初始化游戏棋盘
        
        Args:
            size: 棋盘大小，默认为3x3
        """
        self.size = size
        self.state = np.arange(size * size).reshape((size, size))
        self.empty_pos = (size - 1, size - 1)  # 空格位置
        self.moves = 0  # 移动步数
        
    def get_state(self) -> np.ndarray:
        """获取当前棋盘状态"""
        return self.state.copy()
    
    def get_empty_position(self) -> Tuple[int, int]:
        """获取空格位置"""
        return self.empty_pos
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        检查移动是否有效
        
        Args:
            row: 目标位置的行
            col: 目标位置的列
            
        Returns:
            bool: 移动是否有效
        """
        # 检查位置是否在棋盘范围内
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
            
        # 检查是否与空格相邻
        empty_row, empty_col = self.empty_pos
        return abs(row - empty_row) + abs(col - empty_col) == 1
    
    def move(self, row: int, col: int) -> bool:
        """
        移动指定位置的数字到空格位置
        
        Args:
            row: 要移动的数字的行位置
            col: 要移动的数字的列位置
            
        Returns:
            bool: 移动是否成功
        """
        if not self.is_valid_move(row, col):
            return False
            
        # 交换位置
        empty_row, empty_col = self.empty_pos
        self.state[empty_row, empty_col] = self.state[row, col]
        self.state[row, col] = 0
        self.empty_pos = (row, col)
        self.moves += 1
        return True
        
    def is_solved(self) -> bool:
        """
        检查是否完成游戏
        
        Returns:
            bool: 是否完成
        """
        target = np.arange(self.size * self.size).reshape((self.size, self.size))
        return np.array_equal(self.state, target)
        
    def shuffle(self, moves: int = 100) -> None:
        """
        随机打乱棋盘
        
        Args:
            moves: 随机移动的次数
        """
        for _ in range(moves):
            # 获取可能的移动
            possible_moves = self.get_possible_moves()
            if possible_moves:
                # 随机选择一个移动
                row, col = possible_moves[np.random.randint(len(possible_moves))]
                self.move(row, col)
        self.moves = 0  # 重置移动步数
        
    def get_possible_moves(self) -> List[Tuple[int, int]]:
        """
        获取当前可能的移动位置
        
        Returns:
            List[Tuple[int, int]]: 可移动位置的列表
        """
        moves = []
        empty_row, empty_col = self.empty_pos
        
        # 检查四个方向
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                moves.append((new_row, new_col))
                
        return moves
        
    def is_solvable(self) -> bool:
        """
        检查当前棋盘状态是否可解
        
        Returns:
            bool: 是否可解
        """
        # 将二维数组转换为一维
        flat_state = self.state.flatten()
        
        # 计算逆序数
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] != 0 and flat_state[j] != 0 and flat_state[i] > flat_state[j]:
                    inversions += 1
                    
        # 对于N×N的棋盘，当N为奇数时，逆序数为偶数时有解
        # 当N为偶数时，从底部数空格所在行数的奇偶性与逆序数的奇偶性相同时有解
        if self.size % 2 == 1:
            return inversions % 2 == 0
        else:
            empty_row_from_bottom = self.size - self.empty_pos[0]
            return (inversions + empty_row_from_bottom) % 2 == 0 
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
        # 创建从1开始的数字序列，最后一个是0（空格）
        self.state = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
        self.empty_pos = (size - 1, size - 1)  # 空格位置
        self.moves = 0  # 移动步数
        self.history = []  # 移动历史
        self._save_state()  # 保存初始状态
        
    def reset(self) -> None:
        """重置棋盘状态"""
        size = self.state.shape[0]
        self.state = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
        self.empty_pos = (size - 1, size - 1)  # 空格位置在右下角
        self.moves = 0
        self.history = []  # 清空历史记录
        self._save_state()  # 保存初始状态
        
    def _save_state(self):
        """保存当前状态到历史记录"""
        self.history.append({
            'state': self.state.copy(),
            'empty_pos': self.empty_pos,
            'moves': self.moves
        })
        
    def undo(self) -> bool:
        """
        撤销上一步移动
        
        Returns:
            bool: 是否成功撤销
        """
        if len(self.history) <= 1:  # 只有初始状态
            return False
            
        # 移除当前状态
        self.history.pop()
        # 恢复到上一步状态
        last_state = self.history[-1]
        self.state = last_state['state'].copy()
        self.empty_pos = last_state['empty_pos']
        self.moves = last_state['moves']
        return True
        
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
        temp = self.state[empty_row, empty_col]
        self.state[empty_row, empty_col] = self.state[row, col]
        self.state[row, col] = temp
        self.empty_pos = (row, col)
        self.moves += 1
        self._save_state()  # 保存移动后的状态
        return True
        
    def is_solved(self) -> bool:
        """
        检查当前状态是否为目标状态
        
        Returns:
            bool: 是否为目标状态
        """
        size = self.state.shape[0]
        target = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
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
        检查当前状态是否可解
        
        Returns:
            bool: 是否可解
        """
        try:
            # 获取当前状态和目标状态
            current_state = self.state.copy()
            size = current_state.shape[0]
            target_state = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
            
            # 计算当前状态的逆序数
            current_numbers = []
            for i in range(size):
                for j in range(size):
                    if current_state[i, j] != 0:
                        current_numbers.append(int(current_state[i, j]))  # 转换为 Python int
                        
            current_inversions = 0
            for i in range(len(current_numbers)):
                for j in range(i + 1, len(current_numbers)):
                    if current_numbers[i] > current_numbers[j]:
                        current_inversions += 1
                        
            # 计算目标状态的逆序数
            target_numbers = []
            for i in range(size):
                for j in range(size):
                    if target_state[i, j] != 0:
                        target_numbers.append(int(target_state[i, j]))  # 转换为 Python int
                        
            target_inversions = 0
            for i in range(len(target_numbers)):
                for j in range(i + 1, len(target_numbers)):
                    if target_numbers[i] > target_numbers[j]:
                        target_inversions += 1
                        
            # 对于奇数大小的棋盘，逆序数奇偶性必须相同
            if size % 2 == 1:
                return current_inversions % 2 == target_inversions % 2
            
            # 对于偶数大小的棋盘，还需要考虑空格所在行号
            current_blank_row = None
            target_blank_row = None
            for i in range(size):
                for j in range(size):
                    if int(current_state[i, j]) == 0:
                        current_blank_row = i
                    if int(target_state[i, j]) == 0:
                        target_blank_row = i
                        
            if current_blank_row is None or target_blank_row is None:
                return False
                        
            # 逆序数奇偶性加上空格所在行号的奇偶性必须相同
            return (current_inversions + current_blank_row) % 2 == (target_inversions + target_blank_row) % 2
        except Exception as e:
            print(f"检查可解性时出错：{str(e)}")
            return False 
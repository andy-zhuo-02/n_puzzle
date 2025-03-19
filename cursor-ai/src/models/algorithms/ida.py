import numpy as np
from typing import List, Tuple, Dict, Optional
from ...core.board import Board

class IDAStarSolver:
    """IDA* 算法求解器"""
    
    def __init__(self, board: Board):
        """
        初始化求解器
        
        Args:
            board: 游戏棋盘对象
        """
        self.board = board
        self.size = board.size
        self.goal_state = np.concatenate([np.arange(1, self.size * self.size), [0]]).reshape((self.size, self.size))
        self.goal_positions = self._calculate_goal_positions()
        self.path = []  # 当前搜索路径
        self.moves = []  # 最终解决方案
        
    def _calculate_goal_positions(self) -> Dict[int, Tuple[int, int]]:
        """计算目标状态中每个数字的位置"""
        positions = {}
        for i in range(self.size):
            for j in range(self.size):
                value = self.goal_state[i, j]
                positions[value] = (i, j)
        return positions
        
    def _manhattan_distance(self, state: np.ndarray) -> int:
        """
        计算曼哈顿距离
        
        Args:
            state: 当前状态
            
        Returns:
            int: 曼哈顿距离之和
        """
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                value = state[i, j]
                if value != 0:  # 不计算空格的距离
                    goal_pos = self.goal_positions[value]
                    distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return distance
        
    def _get_neighbors(self, state: np.ndarray) -> List[Tuple[np.ndarray, Tuple[int, int]]]:
        """
        获取相邻状态
        
        Args:
            state: 当前状态
            
        Returns:
            List[Tuple[np.ndarray, Tuple[int, int]]]: 相邻状态列表，每个元素为(新状态, 移动位置)
        """
        neighbors = []
        empty_pos = tuple(np.argwhere(state == 0)[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            new_row, new_col = empty_pos[0] + dr, empty_pos[1] + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_state = state.copy()
                new_state[empty_pos] = new_state[new_row, new_col]
                new_state[new_row, new_col] = 0
                neighbors.append((new_state, (new_row, new_col)))
                
        return neighbors
        
    def _search(self, state: np.ndarray, g: int, bound: int) -> Optional[int]:
        """
        IDA* 搜索函数
        
        Args:
            state: 当前状态
            g: 当前代价
            bound: 当前深度界限
            
        Returns:
            Optional[int]: 找到解返回None，否则返回新的界限
        """
        f = g + self._manhattan_distance(state)
        if f > bound:
            return f
            
        if np.array_equal(state, self.goal_state):
            return None
            
        min_bound = float('inf')
        for next_state, move in self._get_neighbors(state):
            # 避免来回移动
            if len(self.path) > 0 and np.array_equal(next_state, self.path[-1]):
                continue
                
            self.path.append(state)
            self.moves.append(move)
            
            t = self._search(next_state, g + 1, bound)
            
            if t is None:
                return None
                
            min_bound = min(min_bound, t)
            
            self.path.pop()
            self.moves.pop()
            
        return min_bound
        
    def solve(self) -> List[Tuple[int, int]]:
        """
        使用 IDA* 算法求解
        
        Returns:
            List[Tuple[int, int]]: 解决方案的移动序列
        """
        # 首先检查是否可解
        if not self.board.is_solvable():
            return []
            
        initial_state = self.board.get_state()
        if np.array_equal(initial_state, self.goal_state):
            return []
            
        bound = self._manhattan_distance(initial_state)
        self.path = []
        self.moves = []
        
        while True:
            t = self._search(initial_state, 0, bound)
            if t is None:
                return self.moves
            if t == float('inf'):
                return []  # 无解
            bound = t 
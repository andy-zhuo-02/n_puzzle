from collections import deque
import numpy as np
from typing import List, Tuple, Dict, Set
from ...core.board import Board

class BFSSolver:
    """广度优先搜索求解器"""
    
    def __init__(self, board: Board):
        """
        初始化求解器
        
        Args:
            board: 游戏棋盘对象
        """
        self.board = board
        self.size = board.size
        self.goal_state = np.concatenate([np.arange(1, self.size * self.size), [0]]).reshape((self.size, self.size))
        
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
        
    def solve(self) -> List[Tuple[int, int]]:
        """
        使用 BFS 算法求解
        
        Returns:
            List[Tuple[int, int]]: 解决方案的移动序列
        """
        # 首先检查是否可解
        if not self.board.is_solvable():
            return []
            
        initial_state = self.board.get_state()
        if np.array_equal(initial_state, self.goal_state):
            return []
            
        # 使用队列进行BFS
        queue = deque([(initial_state, [], None)])  # (状态, 移动序列, 上一个状态)
        visited = {hash(initial_state.tobytes())}
        
        while queue:
            current_state, moves, prev_state = queue.popleft()
            
            if np.array_equal(current_state, self.goal_state):
                return moves
                
            for next_state, move in self._get_neighbors(current_state):
                state_hash = hash(next_state.tobytes())
                if state_hash not in visited:
                    visited.add(state_hash)
                    queue.append((next_state, moves + [move], current_state))
                    
        return []  # 无解 
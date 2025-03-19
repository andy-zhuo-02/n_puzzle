"""广度优先搜索求解器"""

from typing import List, Tuple, Optional, Dict
from collections import deque
import numpy as np
from ..core.board import Board

def solve_puzzle(board: Board) -> Optional[List[Tuple[int, int]]]:
    """
    使用广度优先搜索算法求解数字华容道
    
    Args:
        board: 游戏棋盘
        
    Returns:
        Optional[List[Tuple[int, int]]]: 解决方案（移动序列），无解返回 None
    """
    # 如果当前状态不可解，直接返回
    if not board.is_solvable():
        return None
        
    # 创建目标状态
    size = board.size
    target = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
    
    # 初始化
    initial_state = board.state.copy()
    initial_pos = board.empty_pos
    
    # 使用队列进行BFS，存储 (状态, 空格位置)
    queue = deque([(initial_state, initial_pos)])
    # 记录已访问状态和前驱状态
    visited = {str(initial_state): None}
    
    # BFS搜索
    while queue:
        state, pos = queue.popleft()
        
        # 检查是否达到目标状态
        if np.array_equal(state, target):
            # 从目标状态回溯到初始状态，构建移动序列
            path = []
            current_state = str(state)
            while visited[current_state] is not None:
                prev_state, prev_pos, move = visited[current_state]
                path.append(move)
                current_state = prev_state
            return path[::-1]  # 反转路径
            
        # 获取所有可能的移动
        row, col = pos
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            
            # 检查移动是否有效
            if 0 <= new_row < size and 0 <= new_col < size:
                # 创建新状态
                new_state = state.copy()
                new_state[row, col] = new_state[new_row, new_col]
                new_state[new_row, new_col] = 0
                
                # 如果是新状态
                state_str = str(new_state)
                if state_str not in visited:
                    visited[state_str] = (str(state), pos, (new_row, new_col))
                    queue.append((new_state, (new_row, new_col)))
                    
    return None  # 无解 
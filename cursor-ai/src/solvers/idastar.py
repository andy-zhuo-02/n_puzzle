"""IDA* 算法求解器"""

from typing import List, Tuple, Optional, Set
import numpy as np
from ..core.board import Board

def manhattan_distance(state: np.ndarray, target: np.ndarray) -> int:
    """
    计算当前状态到目标状态的曼哈顿距离
    
    Args:
        state: 当前状态
        target: 目标状态
        
    Returns:
        int: 曼哈顿距离
    """
    size = state.shape[0]
    distance = 0
    
    # 为每个数字计算其当前位置到目标位置的曼哈顿距离
    for i in range(size):
        for j in range(size):
            if state[i, j] != 0:  # 跳过空格
                # 找到数字在目标状态中的位置
                for ti in range(size):
                    for tj in range(size):
                        if target[ti, tj] == state[i, j]:
                            distance += abs(i - ti) + abs(j - tj)
                            break
                
    return distance

def dfs(state: np.ndarray, pos: Tuple[int, int], g: int, bound: int,
        target: np.ndarray, visited: Set[str], path: List[Tuple[int, int]]) -> Tuple[bool, int]:
    """
    深度优先搜索
    
    Args:
        state: 当前状态
        pos: 空格位置
        g: 当前步数
        bound: 当前深度限制
        target: 目标状态
        visited: 已访问状态集合
        path: 当前路径
        
    Returns:
        Tuple[bool, int]: (是否找到解, 新的深度限制)
    """
    # 计算 f 值
    f = g + manhattan_distance(state, target)
    
    # 如果 f 值超过限制，返回 f 值作为新的限制
    if f > bound:
        return False, f
        
    # 如果达到目标状态，返回成功
    if np.array_equal(state, target):
        return True, bound
        
    # 记录最小的超出限制的 f 值
    min_f = float('inf')
    
    # 获取所有可能的移动
    size = state.shape[0]
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
                visited.add(state_str)
                path.append((new_row, new_col))
                
                # 递归搜索
                found, new_bound = dfs(new_state, (new_row, new_col),
                                     g + 1, bound, target, visited, path)
                
                if found:
                    return True, bound
                    
                # 如果没找到解，更新最小超限值
                min_f = min(min_f, new_bound)
                
                # 回溯
                path.pop()
                visited.remove(state_str)
                
    return False, min_f

def solve_puzzle(board: Board) -> Optional[List[Tuple[int, int]]]:
    """
    使用 IDA* 算法求解数字华容道
    
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
    path = []
    
    # 初始深度限制为曼哈顿距离
    bound = manhattan_distance(initial_state, target)
    
    while bound < float('inf'):
        visited = {str(initial_state)}
        found, new_bound = dfs(initial_state, initial_pos, 0, bound,
                              target, visited, path)
        
        if found:
            return path
            
        if new_bound == float('inf'):
            return None
            
        bound = new_bound
        
    return None 
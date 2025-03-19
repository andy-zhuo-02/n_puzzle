"""A* 算法求解器"""

from typing import List, Tuple, Optional, Dict
import heapq
import numpy as np
from ..core.board import Board

class PuzzleState:
    """数字华容道状态类"""
    def __init__(self, board_array: np.ndarray, empty_pos: Tuple[int, int], 
                 g: int = 0, parent=None, move: Tuple[int, int] = None):
        self.board = board_array
        self.empty_pos = empty_pos
        self.g = g  # 从初始状态到当前状态的实际代价
        self.parent = parent  # 父节点
        self.move = move  # 到达该状态的移动
        self.h = 0  # 启发式估计值
        
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
        
    def __eq__(self, other):
        return np.array_equal(self.board, other.board)
        
    def __hash__(self):
        return hash(str(self.board.tolist()))

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
    
    # 创建目标位置的查找表
    target_positions = {}
    for i in range(size):
        for j in range(size):
            if target[i, j] != 0:  # 跳过空格
                target_positions[target[i, j]] = (i, j)
    
    # 计算每个数字的曼哈顿距离
    for i in range(size):
        for j in range(size):
            if state[i, j] != 0:  # 跳过空格
                ti, tj = target_positions[state[i, j]]
                distance += abs(i - ti) + abs(j - tj)
                
    return distance

def is_goal_state(state: np.ndarray, target: np.ndarray) -> bool:
    """
    检查当前状态是否为目标状态
    
    Args:
        state: 当前状态
        target: 目标状态
        
    Returns:
        bool: 是否为目标状态
    """
    return np.array_equal(state, target)

def get_neighbors(state: PuzzleState, size: int) -> List[PuzzleState]:
    """获取所有可能的下一个状态"""
    neighbors = []
    row, col = state.empty_pos
    
    # 四个可能的移动方向
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        
        # 检查移动是否有效
        if 0 <= new_row < size and 0 <= new_col < size:
            # 创建新状态
            new_board = state.board.copy()
            new_board[row, col] = new_board[new_row, new_col]
            new_board[new_row, new_col] = 0
            
            # 创建新的状态对象
            new_state = PuzzleState(
                new_board,
                (new_row, new_col),
                state.g + 1,
                state,
                (new_row, new_col)
            )
            neighbors.append(new_state)
            
    return neighbors

def build_solution(state: PuzzleState) -> List[Tuple[int, int]]:
    """从目标状态回溯构建解决方案"""
    solution = []
    current = state
    while current.parent is not None:
        solution.append(current.move)
        current = current.parent
    return solution[::-1]

def solve_puzzle(board: Board) -> Optional[List[Tuple[int, int]]]:
    """
    使用 A* 算法求解数字华容道
    
    Args:
        board: 游戏棋盘
        
    Returns:
        Optional[List[Tuple[int, int]]]: 解决方案（移动序列），无解返回 None
    """
    try:
        # 如果当前状态不可解，直接返回
        if not board.is_solvable():
            return None
            
        # 创建目标状态
        size = board.size
        target = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
        
        # 创建初始状态
        initial = PuzzleState(board.state.copy(), board.empty_pos)
        initial.h = manhattan_distance(initial.board, target)
        
        # 检查初始状态是否为目标状态
        if np.array_equal(initial.board, target):
            return []
            
        # 初始化开放列表和关闭列表
        open_list = []
        heapq.heappush(open_list, initial)
        closed_set = set()
        
        while open_list:
            current = heapq.heappop(open_list)
            
            # 如果找到目标状态
            if np.array_equal(current.board, target):
                return build_solution(current)
                
            # 将当前状态添加到关闭列表
            state_hash = hash(current)
            if state_hash in closed_set:
                continue
            closed_set.add(state_hash)
            
            # 扩展当前状态
            for neighbor in get_neighbors(current, size):
                if hash(neighbor) not in closed_set:
                    neighbor.h = manhattan_distance(neighbor.board, target)
                    heapq.heappush(open_list, neighbor)
                    
        return None  # 无解
        
    except Exception as e:
        print(f"A* 算法求解出错：{str(e)}")
        return None 
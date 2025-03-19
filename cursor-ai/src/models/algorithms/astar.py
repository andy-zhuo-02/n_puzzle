import heapq
import numpy as np
from typing import List, Tuple, Dict, Set
from ...core.board import Board

class Node:
    """A* 搜索节点"""
    def __init__(self, state: np.ndarray, parent=None, move=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move  # 从父节点到达此节点的移动
        self.g = g  # 从起始节点到当前节点的实际代价
        self.h = h  # 启发式估计值
        self.f = g + h  # f = g + h
        
    def __lt__(self, other):
        return self.f < other.f
        
    def __eq__(self, other):
        return np.array_equal(self.state, other.state)
        
    def __hash__(self):
        return hash(self.state.tobytes())

class AStarSolver:
    """A* 算法求解器"""
    
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
        
    def _linear_conflict(self, state: np.ndarray) -> int:
        """
        计算线性冲突
        
        Args:
            state: 当前状态
            
        Returns:
            int: 线性冲突数 * 2（因为每个冲突需要额外两步来解决）
        """
        conflicts = 0
        
        # 检查行冲突
        for i in range(self.size):
            for j in range(self.size):
                value1 = state[i, j]
                if value1 == 0:
                    continue
                goal_row1 = self.goal_positions[value1][0]
                if goal_row1 != i:
                    continue
                    
                for k in range(j + 1, self.size):
                    value2 = state[i, k]
                    if value2 == 0:
                        continue
                    goal_row2 = self.goal_positions[value2][0]
                    if goal_row2 == i and value1 > value2:
                        conflicts += 1
                        
        # 检查列冲突
        for j in range(self.size):
            for i in range(self.size):
                value1 = state[i, j]
                if value1 == 0:
                    continue
                goal_col1 = self.goal_positions[value1][1]
                if goal_col1 != j:
                    continue
                    
                for k in range(i + 1, self.size):
                    value2 = state[k, j]
                    if value2 == 0:
                        continue
                    goal_col2 = self.goal_positions[value2][1]
                    if goal_col2 == j and value1 > value2:
                        conflicts += 1
                        
        return conflicts * 2
        
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
        使用 A* 算法求解
        
        Returns:
            List[Tuple[int, int]]: 解决方案的移动序列
        """
        # 首先检查是否可解
        if not self.board.is_solvable():
            return []
            
        initial_state = self.board.get_state()
        if np.array_equal(initial_state, self.goal_state):
            return []
            
        start_node = Node(
            state=initial_state,
            g=0,
            h=self._manhattan_distance(initial_state) + self._linear_conflict(initial_state)
        )
        
        open_set = [start_node]  # 优先队列
        closed_set = set()  # 已访问状态集合
        
        while open_set:
            current = heapq.heappop(open_set)
            
            if np.array_equal(current.state, self.goal_state):
                # 重建移动路径
                moves = []
                while current.parent is not None:
                    moves.append(current.move)
                    current = current.parent
                return moves[::-1]
                
            closed_set.add(hash(current.state.tobytes()))
            
            for neighbor_state, move in self._get_neighbors(current.state):
                if hash(neighbor_state.tobytes()) in closed_set:
                    continue
                    
                g = current.g + 1
                h = self._manhattan_distance(neighbor_state) + self._linear_conflict(neighbor_state)
                
                neighbor = Node(
                    state=neighbor_state,
                    parent=current,
                    move=move,
                    g=g,
                    h=h
                )
                
                # 如果邻居节点已在开放列表中且新路径更好，更新它
                for i, node in enumerate(open_set):
                    if np.array_equal(node.state, neighbor_state) and node.g <= g:
                        break
                else:
                    heapq.heappush(open_set, neighbor)
                    
        return []  # 无解 
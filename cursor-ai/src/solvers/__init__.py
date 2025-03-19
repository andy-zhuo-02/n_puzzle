"""数字华容道求解器模块"""

from .astar import solve_puzzle as astar_solve
from .idastar import solve_puzzle as idastar_solve
from .bfs import solve_puzzle as bfs_solve

__all__ = ['astar_solve', 'idastar_solve', 'bfs_solve'] 
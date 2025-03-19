import unittest
import numpy as np
import time
from src.core.board import Board
from src.models.algorithms import AStarSolver, IDAStarSolver, BFSSolver

class TestSolvers(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.board_3x3 = Board(3)
        self.board_4x4 = Board(4)
        self.timeout = 5  # 设置超时时间为5秒
        
    def _create_board_with_state(self, state: np.ndarray) -> Board:
        """创建具有指定状态的棋盘"""
        board = Board(state.shape[0])
        board.state = state.copy()
        # 更新空格位置
        empty_pos = tuple(np.argwhere(state == 0)[0])
        board.empty_pos = empty_pos
        return board
        
    def test_already_solved(self):
        """测试已经解决的情况"""
        # 3x3 目标状态
        target_3x3 = np.concatenate([np.arange(1, 9), [0]]).reshape(3, 3)
        board = self._create_board_with_state(target_3x3)
        
        solvers = [
            AStarSolver(board),
            IDAStarSolver(board),
            BFSSolver(board)
        ]
        
        for solver in solvers:
            solution = solver.solve()
            self.assertEqual(len(solution), 0, 
                           f"{solver.__class__.__name__} 对已解决状态应返回空列表")
            
    def test_simple_case(self):
        """测试简单情况（只需要1-2步）"""
        # 3x3 棋盘，只需要移动一步
        # 1 2 3
        # 4 5 6
        # 7 0 8
        initial_state = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ])
        board = self._create_board_with_state(initial_state)
        
        solvers = [
            AStarSolver(board),
            IDAStarSolver(board),
            BFSSolver(board)
        ]
        
        for solver in solvers:
            solution = solver.solve()
            self.assertEqual(len(solution), 1, 
                           f"{solver.__class__.__name__} 应该只需要1步")
            
    def test_medium_case(self):
        """测试中等难度情况"""
        # 3x3 棋盘，需要多步移动
        # 1 2 3
        # 4 0 6
        # 7 5 8
        initial_state = np.array([
            [1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]
        ])
        board = self._create_board_with_state(initial_state)
        
        solvers = [
            AStarSolver(board),
            IDAStarSolver(board),
            BFSSolver(board)
        ]
        
        for solver in solvers:
            solution = solver.solve()
            self.assertGreater(len(solution), 0, 
                             f"{solver.__class__.__name__} 应该找到解决方案")
            # 验证每一步移动都是有效的
            current_state = initial_state.copy()
            for move in solution:
                row, col = move
                empty_pos = tuple(np.argwhere(current_state == 0)[0])
                # 确保移动是相邻的
                self.assertEqual(abs(row - empty_pos[0]) + abs(col - empty_pos[1]), 1,
                               f"{solver.__class__.__name__} 产生了无效移动")
                # 执行移动
                current_state[empty_pos] = current_state[row, col]
                current_state[row, col] = 0
                
            # 验证最终状态是否正确
            target_state = np.concatenate([np.arange(1, 9), [0]]).reshape(3, 3)
            np.testing.assert_array_equal(current_state, target_state,
                                        f"{solver.__class__.__name__} 没有达到目标状态")
            
    def test_unsolvable_case(self):
        """测试无解情况"""
        # 测试多个无解状态
        unsolvable_states = [
            # 3x3 棋盘，无解状态1：交换了7和8
            np.array([
                [1, 2, 3],
                [4, 5, 6],
                [8, 7, 0]
            ]),
            # 3x3 棋盘，无解状态2：交换了1和2
            np.array([
                [2, 1, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]),
            # 4x4 棋盘，无解状态
            np.array([
                [1,  2,  3,  4],
                [5,  6,  7,  8],
                [9,  10, 11, 12],
                [13, 15, 14, 0]
            ])
        ]
        
        for initial_state in unsolvable_states:
            board = self._create_board_with_state(initial_state)
            
            # 首先验证棋盘状态确实是无解的
            self.assertFalse(board.is_solvable(), 
                           f"状态应该是无解的：\n{initial_state}")
            
            solvers = [
                AStarSolver(board),
                IDAStarSolver(board),
                BFSSolver(board)
            ]
            
            for solver in solvers:
                start_time = time.time()
                solution = solver.solve()
                end_time = time.time()
                
                # 验证返回空列表
                self.assertEqual(len(solution), 0, 
                               f"{solver.__class__.__name__} 对无解状态应返回空列表")
                
                # 验证在合理时间内返回（应该很快，因为会在开始时就判断无解）
                elapsed_time = end_time - start_time
                self.assertLess(elapsed_time, 0.1,  # 由于是快速判断，0.1秒就足够了
                              f"{solver.__class__.__name__} 在处理无解状态时耗时过长 ({elapsed_time:.3f}秒)")
                              
    def test_solvable_check(self):
        """测试可解性检查"""
        # 测试可解状态
        solvable_states = [
            # 3x3 标准目标状态
            np.array([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]),
            # 3x3 简单打乱状态
            np.array([
                [1, 2, 3],
                [4, 5, 6],
                [7, 0, 8]
            ]),
            # 4x4 标准目标状态
            np.array([
                [1,  2,  3,  4],
                [5,  6,  7,  8],
                [9,  10, 11, 12],
                [13, 14, 15, 0]
            ])
        ]
        
        for state in solvable_states:
            board = self._create_board_with_state(state)
            self.assertTrue(board.is_solvable(), 
                          f"状态应该是可解的：\n{state}")
            
    def test_4x4_simple_case(self):
        """测试4x4棋盘的简单情况"""
        # 4x4 棋盘，只需要移动一步
        # 1  2  3  4
        # 5  6  7  8
        # 9  10 11 12
        # 13 14 0  15
        initial_state = np.array([
            [1,  2,  3,  4],
            [5,  6,  7,  8],
            [9,  10, 11, 12],
            [13, 14, 0,  15]
        ])
        board = self._create_board_with_state(initial_state)
        
        solvers = [
            AStarSolver(board),
            IDAStarSolver(board),
            BFSSolver(board)
        ]
        
        for solver in solvers:
            solution = solver.solve()
            self.assertEqual(len(solution), 1, 
                           f"{solver.__class__.__name__} 应该只需要1步")
            
    def test_invalid_moves(self):
        """测试无效移动的处理"""
        # 创建一个3x3棋盘
        board = Board(3)
        solvers = [
            AStarSolver(board),
            IDAStarSolver(board),
            BFSSolver(board)
        ]
        
        for solver in solvers:
            # 获取空格位置
            empty_pos = tuple(np.argwhere(board.state == 0)[0])
            # 获取所有可能的移动
            neighbors = solver._get_neighbors(board.state)
            # 验证所有移动都是有效的（与空格相邻）
            for state, move in neighbors:
                row, col = move
                self.assertEqual(abs(row - empty_pos[0]) + abs(col - empty_pos[1]), 1,
                               f"{solver.__class__.__name__} 产生了无效移动")
                
if __name__ == '__main__':
    unittest.main() 
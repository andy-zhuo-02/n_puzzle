from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from typing import List, Tuple, Optional
import threading
import time
import numpy as np
from ..core.board import Board
from ..solvers.astar import solve_puzzle as astar_solve
from ..solvers.idastar import solve_puzzle as idastar_solve
from ..solvers.bfs import solve_puzzle as bfs_solve

class AIPlayer(QObject):
    """AI 玩家类，负责自动解题"""
    
    # 信号定义
    solution_found = pyqtSignal(list)  # 参数：解决方案（移动序列）
    solution_not_found = pyqtSignal()
    move_made = pyqtSignal(tuple)  # 参数：移动位置 (row, col)
    solution_completed = pyqtSignal()
    
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.solution = []  # 当前解决方案
        self.current_step = 0  # 当前演示步骤
        self.demo_timer = QTimer()  # 演示计时器
        self.demo_timer.timeout.connect(self._make_next_move)
        self.solving_thread = None  # 求解线程
        self.timeout = 10  # 求解超时时间（秒）
        
    def solve(self, algorithm: str):
        """
        使用指定算法求解
        
        Args:
            algorithm: 算法名称（"A*"、"IDA*"、"BFS"）
        """
        # 检查当前状态是否可解
        if not self.board.is_solvable():
            self.solution_not_found.emit()
            return
            
        # 选择算法
        if algorithm == "A*":
            solver = astar_solve
        elif algorithm == "IDA*":
            solver = idastar_solve
        elif algorithm == "BFS":
            solver = bfs_solve
        else:
            raise ValueError(f"未知算法：{algorithm}")
            
        # 在新线程中运行求解过程
        self.solving_thread = threading.Thread(
            target=self._solve_in_thread,
            args=(solver,)
        )
        self.solving_thread.daemon = True
        self.solving_thread.start()
            
    def _solve_in_thread(self, solver):
        """
        在线程中运行求解过程
        
        Args:
            solver: 求解函数
        """
        try:
            # 创建事件用于超时检测
            done_event = threading.Event()
            # 使用列表存储解决方案和错误信息
            solution = [None]
            error = [None]
            
            def solve_task():
                try:
                    # 检查当前状态是否可解
                    if not self.board.is_solvable():
                        error[0] = "当前状态无解"
                        done_event.set()
                        return
                        
                    # 获取当前状态和目标状态
                    current_state = self.board.get_state()
                    size = current_state.shape[0]
                    target_state = np.concatenate([np.arange(1, size * size), [0]]).reshape((size, size))
                    
                    # 检查当前状态是否已经是目标状态
                    if np.array_equal(current_state, target_state):
                        solution[0] = []  # 空列表表示已经完成
                    else:
                        try:
                            result = solver(self.board)
                            if result is None:
                                error[0] = "无法找到解决方案"
                            else:
                                solution[0] = result
                        except Exception as e:
                            error[0] = str(e)
                    done_event.set()
                except Exception as e:
                    error[0] = str(e)
                    done_event.set()
            
            # 创建并启动线程
            thread = threading.Thread(target=solve_task)
            thread.daemon = True
            thread.start()
            
            # 等待线程完成或超时
            if not done_event.wait(timeout=self.timeout):
                self.solving_thread = None
                self.solution_not_found.emit()
                return
                
            # 检查是否有错误
            if error[0] is not None:
                self.solving_thread = None
                self.solution_not_found.emit()
                return
                
            # 检查是否找到解
            if solution[0] is None:
                self.solving_thread = None
                self.solution_not_found.emit()
                return
                
            # 发送解决方案
            self.solving_thread = None
            self.solution = solution[0]
            self.solution_found.emit(solution[0])
        except Exception as e:
            print(f"求解线程出错：{str(e)}")
            self.solving_thread = None
            self.solution_not_found.emit()
            
    def start_demo(self, interval: int):
        """
        开始演示解决方案
        
        Args:
            interval: 移动间隔（毫秒）
        """
        if not self.solution:
            return
            
        self.current_step = 0
        self.demo_timer.setInterval(interval)
        self.demo_timer.start()
        
    def stop_demo(self):
        """停止演示"""
        self.demo_timer.stop()
        self.solution = []
        self.current_step = 0
        
        # 如果正在求解，停止求解线程
        if self.solving_thread and self.solving_thread.is_alive():
            self.solving_thread = None
        
    def set_interval(self, interval: int):
        """
        设置演示速度
        
        Args:
            interval: 移动间隔（毫秒）
        """
        self.demo_timer.setInterval(interval)
        
    def _make_next_move(self):
        """执行下一步移动"""
        if not self.solution or self.current_step >= len(self.solution):
            self.stop_demo()
            self.solution_completed.emit()
            return
            
        # 执行移动
        move = self.solution[self.current_step]
        self.move_made.emit(move)
        self.current_step += 1 
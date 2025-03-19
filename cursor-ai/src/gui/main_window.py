from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor
from .board import BoardWidget
from .controls import ControlPanel, AIControlPanel
from .dialogs import WinDialog, show_error
from ..core.board import Board
from ..core.game import Game
from ..models.ai_player import AIPlayer

class MainWindow(QMainWindow):
    """游戏主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数字华容道")
        self.board = Board()
        self.game = Game()
        self.game.add_listener(self._on_game_event)  # 添加游戏事件监听
        self._init_ui()
        self._init_timer()
        self._init_ai()
        self._on_new_game()  # 开始新游戏
        
    def _init_ui(self):
        """初始化UI"""
        self.setMinimumSize(800, 600)
        
        # 设置窗口背景色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f2f5"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建游戏区域
        game_area = QWidget()
        game_layout = QVBoxLayout()
        game_layout.setSpacing(10)
        
        # 添加标题
        title_label = QLabel("数字华容道")
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 32px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_layout.addWidget(title_label)
        
        # 创建棋盘
        self.board_widget = BoardWidget(self.board)
        self.board_widget.set_tile_size(120)
        self.board_widget.tile_clicked.connect(self._on_tile_clicked)
        game_layout.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        game_area.setLayout(game_layout)
        main_layout.addWidget(game_area, stretch=2)
        
        # 创建控制面板
        control_area = QWidget()
        control_layout = QVBoxLayout()
        
        self.control_panel = ControlPanel()
        self.ai_control_panel = AIControlPanel()
        
        control_layout.addWidget(self.control_panel)
        control_layout.addWidget(self.ai_control_panel)
        control_layout.addStretch()
        
        control_area.setLayout(control_layout)
        main_layout.addWidget(control_area, stretch=1)
        
        central_widget.setLayout(main_layout)
        
        # 连接信号
        self.control_panel.new_game_requested.connect(self._on_new_game)
        self.control_panel.reset_requested.connect(self._on_reset)
        self.control_panel.undo_requested.connect(self._on_undo)
        self.control_panel.help_requested.connect(self._on_help)
        self.control_panel.difficulty_changed.connect(self._on_difficulty_changed)
        
        self.ai_control_panel.solve_requested.connect(self._on_solve_requested)
        self.ai_control_panel.stop_requested.connect(self._on_stop_requested)
        self.ai_control_panel.speed_changed.connect(self._on_speed_changed)
        
    def _init_timer(self):
        """初始化计时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.start_time = 0
        self.elapsed_time = 0
        
    def _init_ai(self):
        """初始化 AI 玩家"""
        self.ai_player = AIPlayer(self.board)
        
        # 连接 AI 玩家信号
        self.ai_player.solution_found.connect(self._on_solution_found)
        self.ai_player.solution_not_found.connect(self._on_solution_not_found)
        self.ai_player.move_made.connect(self._on_ai_move_made)
        self.ai_player.solution_completed.connect(self._on_solution_completed)
        
    def _start_timer(self):
        """开始计时"""
        self.elapsed_time = 0
        self.control_panel.update_info(0, self.elapsed_time)
        self.timer.start(1000)  # 每秒更新一次
        
    def _stop_timer(self):
        """停止计时"""
        self.timer.stop()
        
    def _update_time(self):
        """更新时间显示"""
        self.elapsed_time += 1
        self.control_panel.update_info(self.game.steps, self.elapsed_time)
        
    def _on_tile_clicked(self, row: int, col: int):
        """处理方块点击事件"""
        if self.game.move(row, col):
            # 同步 Board 状态
            self.board.state = self.game.board.state.copy()
            self.board.empty_pos = self.game.board.empty_pos
            self.board.moves = self.game.steps
            self.board_widget.update()
            
    def _on_new_game(self):
        """处理新游戏按钮点击事件"""
        # 先重置游戏状态
        self.game.new_game()
        # 打乱棋盘
        self.game.board.shuffle()
        # 同步 Board 状态
        self.board.state = self.game.board.state.copy()
        self.board.empty_pos = self.game.board.empty_pos
        self.board.moves = self.game.steps
        # 更新界面
        self.board_widget.update()
        self.ai_control_panel.reset_state()
        self._start_timer()
        
    def _on_reset(self):
        """处理重置按钮点击事件"""
        # 重置游戏状态
        self.game.reset()
        # 同步 Board 状态
        self.board.state = self.game.board.state.copy()
        self.board.empty_pos = self.game.board.empty_pos
        self.board.moves = self.game.steps
        # 更新界面
        self.board_widget.update()
        self.ai_control_panel.reset_state()
        self._start_timer()
        
    def _on_undo(self):
        """处理撤销按钮点击事件"""
        if self.game.is_running:
            if self.game.undo():
                # 同步 Board 状态
                self.board.state = self.game.board.state.copy()
                self.board.empty_pos = self.game.board.empty_pos
                self.board_widget.update()
            
    def _on_help(self):
        """处理帮助按钮点击事件"""
        import os
        import webbrowser
        
        # 获取手册文件的路径
        manual_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'docs',
            'manual.md'
        )
        
        # 如果文件存在，使用默认浏览器打开
        if os.path.exists(manual_path):
            webbrowser.open('file://' + manual_path)
        else:
            show_error(self, "找不到游戏手册文件！")
        
    def _on_difficulty_changed(self, difficulty: int):
        """难度改变处理"""
        # 先重置游戏状态
        self.game.new_game()
        # 打乱棋盘
        self.game.board.shuffle(difficulty * 10)
        # 同步 Board 状态
        self.board.state = self.game.board.state.copy()
        self.board.empty_pos = self.game.board.empty_pos
        self.board.moves = self.game.steps
        # 更新界面
        self.board_widget.update()
        
    def _on_solve_requested(self, algorithm: str):
        """AI 求解请求处理"""
        try:
            self.ai_player.solve(algorithm)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"求解过程出错：{str(e)}")
            self.ai_control_panel.reset_state()
            
    def _on_stop_requested(self):
        """停止 AI 演示处理"""
        self.ai_player.stop_demo()
        
    def _on_speed_changed(self, interval: int):
        """演示速度改变处理"""
        self.ai_player.set_interval(interval)
        
    def _on_solution_found(self, solution):
        """找到解决方案处理"""
        interval = self.ai_control_panel.get_move_interval()
        self.ai_player.start_demo(interval)
        
    def _on_solution_not_found(self):
        """未找到解决方案处理"""
        QMessageBox.information(self, "提示", "当前状态无解")
        self.ai_control_panel.reset_state()
        
    def _on_ai_move_made(self, move):
        """AI 移动处理"""
        row, col = move
        if self.game.move(row, col):
            # 同步 Board 状态
            self.board.state = self.game.board.state.copy()
            self.board.empty_pos = self.game.board.empty_pos
            self.board.moves = self.game.steps
            self.board_widget.update()
            self.control_panel.update_info(self.game.steps, self.elapsed_time)
        
    def _on_solution_completed(self):
        """解决方案演示完成处理"""
        self.ai_control_panel.reset_state()
        QMessageBox.information(self, "提示", "演示完成！")
        
    def _on_game_event(self, event_type: str, **kwargs):
        """处理游戏事件"""
        if event_type == "move":
            self.control_panel.update_info(self.game.steps, self.elapsed_time)
        elif event_type == "game_over":
            self._stop_timer()
            dialog = WinDialog(self.game.steps, self.elapsed_time, self)
            if dialog.exec() == WinDialog.DialogCode.Accepted:
                self._on_new_game() 
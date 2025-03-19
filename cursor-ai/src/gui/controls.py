from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSpinBox, QComboBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal

class ControlPanel(QWidget):
    """控制面板界面组件"""
    
    # 信号定义
    new_game_requested = pyqtSignal()
    reset_requested = pyqtSignal()
    undo_requested = pyqtSignal()
    help_requested = pyqtSignal()
    difficulty_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 游戏信息显示
        info_layout = QHBoxLayout()
        self.moves_label = QLabel("步数: 0")
        self.time_label = QLabel("时间: 0.0秒")
        info_layout.addWidget(self.moves_label)
        info_layout.addWidget(self.time_label)
        layout.addLayout(info_layout)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        self.new_game_btn = QPushButton("新游戏")
        self.reset_btn = QPushButton("重置")
        self.undo_btn = QPushButton("撤销")
        self.help_btn = QPushButton("帮助")
        
        # 连接按钮信号
        self.new_game_btn.clicked.connect(self.new_game_requested)
        self.reset_btn.clicked.connect(self.reset_requested)
        self.undo_btn.clicked.connect(self.undo_requested)
        self.help_btn.clicked.connect(self.help_requested)
        
        button_layout.addWidget(self.new_game_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.undo_btn)
        button_layout.addWidget(self.help_btn)
        layout.addLayout(button_layout)
        
        # 难度选择
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(QLabel("难度:"))
        self.difficulty_spin = QSpinBox()
        self.difficulty_spin.setRange(1, 3)
        self.difficulty_spin.setValue(2)
        self.difficulty_spin.setPrefix("级别")
        self.difficulty_spin.valueChanged.connect(self.difficulty_changed)
        difficulty_layout.addWidget(self.difficulty_spin)
        layout.addLayout(difficulty_layout)
        
        self.setLayout(layout)
        
    def update_info(self, moves: int, time: float):
        """
        更新游戏信息显示
        
        Args:
            moves: 当前步数
            time: 已用时间
        """
        self.moves_label.setText(f"步数: {moves}")
        self.time_label.setText(f"时间: {time:.1f}秒")
        
    def get_difficulty(self) -> int:
        """获取当前选择的难度级别"""
        return self.difficulty_spin.value()

class AIControlPanel(QGroupBox):
    """AI 控制面板"""
    
    # 信号定义
    solve_requested = pyqtSignal(str)  # 参数：选择的算法
    stop_requested = pyqtSignal()
    speed_changed = pyqtSignal(int)  # 参数：移动间隔（毫秒）
    
    def __init__(self, parent=None):
        super().__init__("AI 助手", parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()
        
        # 算法选择
        algo_layout = QHBoxLayout()
        algo_label = QLabel("算法:")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["A*", "IDA*", "BFS"])
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)
        layout.addLayout(algo_layout)
        
        # 演示速度控制
        speed_layout = QHBoxLayout()
        speed_label = QLabel("演示速度:")
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(100, 2000)  # 100ms - 2000ms
        self.speed_spin.setSingleStep(100)
        self.speed_spin.setValue(500)  # 默认 500ms
        self.speed_spin.valueChanged.connect(self.speed_changed)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_spin)
        layout.addLayout(speed_layout)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        self.solve_button = QPushButton("求解")
        self.stop_button = QPushButton("停止")
        self.stop_button.setEnabled(False)
        
        self.solve_button.clicked.connect(self._on_solve_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        
        button_layout.addWidget(self.solve_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def _on_solve_clicked(self):
        """求解按钮点击处理"""
        self.solve_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.algo_combo.setEnabled(False)
        self.solve_requested.emit(self.algo_combo.currentText())
        
    def _on_stop_clicked(self):
        """停止按钮点击处理"""
        self.solve_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.algo_combo.setEnabled(True)
        self.stop_requested.emit()
        
    def reset_state(self):
        """重置控件状态"""
        self.solve_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.algo_combo.setEnabled(True)
        
    def get_move_interval(self) -> int:
        """获取移动间隔时间（毫秒）"""
        return self.speed_spin.value() 
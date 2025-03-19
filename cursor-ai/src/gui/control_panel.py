from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

class ControlPanel(QWidget):
    """控制面板组件"""
    
    new_game_clicked = pyqtSignal()
    undo_clicked = pyqtSignal()
    help_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        # 设置背景色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建状态信息区域
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        status_layout = QVBoxLayout()
        status_layout.setSpacing(10)
        
        # 步数显示
        steps_layout = QHBoxLayout()
        steps_label = QLabel("步数:")
        steps_label.setStyleSheet("color: #495057; font-weight: bold;")
        self.steps_label = QLabel("0")
        self.steps_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        steps_layout.addWidget(steps_label)
        steps_layout.addWidget(self.steps_label)
        steps_layout.addStretch()
        status_layout.addLayout(steps_layout)
        
        # 时间显示
        time_layout = QHBoxLayout()
        time_label = QLabel("时间:")
        time_label.setStyleSheet("color: #495057; font-weight: bold;")
        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_label)
        time_layout.addStretch()
        status_layout.addLayout(time_layout)
        
        status_frame.setLayout(status_layout)
        layout.addWidget(status_frame)
        
        # 创建按钮区域
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # 新游戏按钮
        self.new_game_btn = QPushButton("新游戏")
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
                border: 2px solid #4CAF50;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.new_game_btn.clicked.connect(self.new_game_clicked.emit)
        button_layout.addWidget(self.new_game_btn)
        
        # 撤销按钮
        self.undo_btn = QPushButton("撤销")
        self.undo_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
                border: 2px solid #2196F3;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.undo_btn.clicked.connect(self.undo_clicked.emit)
        button_layout.addWidget(self.undo_btn)
        
        # 帮助按钮
        self.help_btn = QPushButton("帮助")
        self.help_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
                border: 2px solid #FF9800;
            }
            QPushButton:pressed {
                background-color: #EF6C00;
            }
        """)
        self.help_btn.clicked.connect(self.help_clicked.emit)
        button_layout.addWidget(self.help_btn)
        
        button_frame.setLayout(button_layout)
        layout.addWidget(button_frame)
        
        # 添加弹性空间
        layout.addStretch()
        
        self.setLayout(layout)
        
    def update_steps(self, steps: int):
        """更新步数显示"""
        self.steps_label.setText(str(steps))
        
    def update_time(self, seconds: int):
        """更新时间显示"""
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        self.time_label.setText(f"{minutes:02d}:{remaining_seconds:02d}")
        
    def set_undo_enabled(self, enabled: bool):
        """设置撤销按钮状态"""
        self.undo_btn.setEnabled(enabled)
        if enabled:
            self.undo_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                    border: 2px solid #2196F3;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
        else:
            self.undo_btn.setStyleSheet("""
                QPushButton {
                    background-color: #BDBDBD;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                    font-weight: bold;
                }
            """) 
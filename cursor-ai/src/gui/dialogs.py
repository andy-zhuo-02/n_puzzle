from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt

class WinDialog(QDialog):
    """游戏胜利对话框"""
    
    def __init__(self, steps: int, time: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("恭喜")
        self.setFixedWidth(300)
        self._init_ui(steps, time)
        
    def _init_ui(self, steps: int, time: int):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 显示步数和时间
        info_label = QLabel(f"步数: {steps}\n时间: {time//60:02d}:{time%60:02d}")
        info_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 再来一局按钮
        again_btn = QPushButton("再来一局")
        again_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        again_btn.clicked.connect(self.accept)
        button_layout.addWidget(again_btn)
        
        # 退出按钮
        exit_btn = QPushButton("退出")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        exit_btn.clicked.connect(self.reject)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("游戏设置")
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        
        # 添加设置选项
        # TODO: 添加更多设置选项
        
        # 按钮
        button = QPushButton("确定")
        button.clicked.connect(self.accept)
        layout.addWidget(button)
        
        self.setLayout(layout)

def show_error(parent, message: str):
    """显示错误对话框"""
    QMessageBox.critical(parent, "错误", message) 
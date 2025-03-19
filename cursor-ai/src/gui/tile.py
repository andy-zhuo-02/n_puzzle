from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import QFont, QColor

class Tile(QPushButton):
    """数字方块类"""
    
    def __init__(self, number: int, parent=None):
        super().__init__(parent)
        self.number = number
        self._init_ui()
        self.animation = None
        
    def _init_ui(self):
        """初始化UI"""
        if self.number == 0:
            self.setText("")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f8f9fa;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                }
            """)
        else:
            self.setText(str(self.number))
            # 根据数字设置不同的颜色
            colors = {
                1: "#FF6B6B",  # 红色
                2: "#4ECDC4",  # 青色
                3: "#45B7D1",  # 蓝色
                4: "#96CEB4",  # 绿色
                5: "#FFEEAD",  # 黄色
                6: "#D4A5A5",  # 粉色
                7: "#9B59B6",  # 紫色
                8: "#3498DB",  # 深蓝色
            }
            color = colors.get(self.number, "#2ECC71")  # 默认绿色
            
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                    border: 2px solid {color}aa;
                }}
                QPushButton:pressed {{
                    background-color: {color}aa;
                }}
            """)
            
        # 设置字体
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.setFont(font)
        
    def animate_move(self, target_pos: QPoint, duration: int = 200):
        """
        创建移动动画
        
        Args:
            target_pos: 目标位置
            duration: 动画持续时间（毫秒）
        """
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(target_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start() 
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColor
from .tile import Tile
from ..core.board import Board
from functools import partial

class BoardWidget(QWidget):
    """游戏棋盘界面组件"""
    
    tile_clicked = pyqtSignal(int, int)  # 发送点击的方块位置
    
    def __init__(self, board: Board, parent=None):
        super().__init__(parent)
        self.board = board
        self.tiles = {}  # 存储数字方块，使用位置作为键
        self.tile_size = 120  # 默认方块大小
        self._init_ui()
        self.update()
        
    def _init_ui(self):
        """初始化UI"""
        # 设置背景色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f2f5"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        # 设置布局
        layout = QGridLayout()
        layout.setSpacing(4)  # 增加方块之间的间距
        layout.setContentsMargins(8, 8, 8, 8)  # 设置边距
        self.setLayout(layout)
        
    def set_tile_size(self, size: int):
        """设置方块大小"""
        self.tile_size = size
        self.update()
        
    def update(self):
        """更新棋盘显示"""
        # 计算总大小，包括间距和边距
        size = self.board.size
        total_size = self.tile_size * size + 4 * (size - 1) + 16  # 16是边距
        self.setFixedSize(total_size, total_size)
        
        # 先清理旧的方块
        self.clear()
        
        # 获取当前状态
        state = self.board.state
        
        # 创建新的方块
        for i in range(size):
            for j in range(size):
                number = state[i][j]
                if number == 0:
                    continue
                    
                # 创建新方块
                tile = Tile(number)
                tile.setFixedSize(self.tile_size, self.tile_size)
                # 使用 partial 来固定参数
                tile.clicked.connect(partial(self.tile_clicked.emit, i, j))
                self.tiles[(i, j)] = tile
                self.layout().addWidget(tile, i, j)
                    
    def clear(self):
        """清空棋盘"""
        for tile in self.tiles.values():
            self.layout().removeWidget(tile)
            tile.deleteLater()
        self.tiles.clear() 
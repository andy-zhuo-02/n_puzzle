"""游戏配置文件"""

# 游戏基本设置
DEFAULT_BOARD_SIZE = 3
MIN_BOARD_SIZE = 2
MAX_BOARD_SIZE = 5

# 游戏难度设置
DIFFICULTY_LEVELS = {
    'easy': 20,    # 简单模式随机移动次数
    'medium': 50,  # 中等模式随机移动次数
    'hard': 100    # 困难模式随机移动次数
}

# AI设置
AI_MOVE_DELAY = 0.5  # AI移动之间的延迟（秒）
MAX_SEARCH_DEPTH = 1000  # 最大搜索深度

# 界面设置
TILE_SIZE = 100  # 方块大小（像素）
TILE_MARGIN = 5  # 方块之间的间距（像素）
ANIMATION_DURATION = 200  # 动画持续时间（毫秒）

# 颜色设置
COLORS = {
    'background': '#F0F0F0',
    'tile': '#4CAF50',
    'tile_text': '#FFFFFF',
    'empty': '#FFFFFF',
    'highlight': '#81C784'
}

# 存储设置
SAVE_FILE = 'game_save.json'
HIGH_SCORES_FILE = 'high_scores.db' 
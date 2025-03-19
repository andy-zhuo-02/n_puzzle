from core.game import Game

def main():
    """主程序入口"""
    # 创建游戏实例
    game = Game(3)
    
    # 注册回调函数
    def on_move():
        state, empty_pos = game.get_board_state()
        print(f"\n当前步数: {game.get_moves()}")
        print(f"已用时间: {game.get_elapsed_time():.1f}秒")
        print_board(state)
        
    def on_win():
        print("\n恭喜！你完成了游戏！")
        print(f"总步数: {game.get_moves()}")
        print(f"总用时: {game.get_elapsed_time():.1f}秒")
        
    def on_reset():
        print("\n游戏开始！")
        state, _ = game.get_board_state()
        print_board(state)
    
    game.register_callback('on_move', on_move)
    game.register_callback('on_win', on_win)
    game.register_callback('on_reset', on_reset)
    
    # 开始游戏
    game.start_game()
    
    # 游戏主循环
    while game.is_running:
        try:
            move = input("\n请输入要移动的数字（或'q'退出）: ")
            if move.lower() == 'q':
                break
                
            number = int(move)
            state, _ = game.get_board_state()
            # 查找数字位置
            found = False
            for i in range(3):
                for j in range(3):
                    if state[i][j] == number:
                        game.make_move(i, j)
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"找不到数字 {number}！")
        except ValueError:
            print("无效输入！请输入数字或'q'退出。")
        except Exception as e:
            print(f"错误：{e}")

def print_board(state):
    """
    打印棋盘状态
    
    Args:
        state: 棋盘状态矩阵
    """
    # 计算最大数字的宽度
    max_width = len(str(len(state) * len(state) - 1))
    # 计算分隔线的长度（每个数字格子宽度 + 边框）
    line_length = (max_width + 2) * len(state) + len(state) + 1
    
    # 打印分隔线
    print("-" * line_length)
    
    # 打印每一行
    for row in state:
        print("|", end="")
        for num in row:
            if num == 0:
                # 空格位置打印空格
                print(" " * (max_width + 2), end="|")
            else:
                # 数字右对齐显示
                print(f" {str(num).rjust(max_width)} ", end="|")
        print("\n" + "-" * line_length)

if __name__ == "__main__":
    main() 
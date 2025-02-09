import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces

class DigitalHuRongEnv(gym.Env):
    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 4}
    
    def __init__(self, size=2, render_mode=None):
        super().__init__()
        self.size = size
        self.window_size = 512
        self.action_space = spaces.Discrete(4)  # 0:上 1:右 2:下 3:左
        self.observation_space = spaces.Box(low=0, high=size*size-1, shape=(size*size,), dtype=np.int64)
        
        self._action_to_direction = {
            0: (-1, 0),
            1: (0, 1),
            2: (1, 0),
            3: (0, -1),
        }
        
        self.render_mode = render_mode
        self.window = None
        self.clock = None
        self.blank_pos = None
        
        # 显式初始化Pygame
        if self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            self.clock = pygame.time.Clock()
        
        self.goal = np.append(np.arange(1, size*size), 0).reshape(size, size)

        self.reset()

    def _get_obs(self):
        return self.board.flatten()
    
    def _get_info(self):
        return {"distance": np.sum(self.board != self.goal)}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = self.goal.copy()
        self.blank_pos = np.argwhere(self.board == 0)[0]
        
        # 生成有效初始状态
        for _ in range(100):
            valid_actions = [
                a for a in range(4) 
                if self._is_valid_move(self.blank_pos + self._action_to_direction[a])
            ]
            action = self.np_random.choice(valid_actions)
            self._move(action)
            
        return self._get_obs(), self._get_info()

    def _is_valid_move(self, new_blank):
        return 0 <= new_blank[0] < self.size and 0 <= new_blank[1] < self.size

    def _move(self, action):
        direction = self._action_to_direction[action]
        new_blank = self.blank_pos + direction
        
        if self._is_valid_move(new_blank):
            i, j = self.blank_pos
            ni, nj = new_blank
            self.board[i, j], self.board[ni, nj] = self.board[ni, nj], self.board[i, j]
            self.blank_pos = new_blank
            return True
        return False

    def step(self, action):
        valid = self._move(action)
        reward = -0.1 if valid else -1
        terminated = np.array_equal(self.board, self.goal)
        if terminated:
            reward = 10
        return self._get_obs(), reward, terminated, False, self._get_info()

    def render(self):
        if self.render_mode == "human" and self.window is not None:
            self._draw_board()

    def _draw_board(self):
        cell_size = self.window_size // self.size
        self.window.fill((255, 255, 255))
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == 0:
                    color = (200, 200, 200)
                else:
                    color = (100, 150, 200)
                
                rect = pygame.Rect(j*cell_size, i*cell_size, cell_size-2, cell_size-2)
                pygame.draw.rect(self.window, color, rect)
                
                if self.board[i, j] != 0:
                    font = pygame.font.Font(None, 100)
                    text = font.render(str(self.board[i, j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.window.blit(text, text_rect)
        
        pygame.display.flip()
        self.clock.tick(self.metadata['render_fps'])

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

class GameInterface:
    def __init__(self, model=None):
        self.env = DigitalHuRongEnv(render_mode="human", size=3)  # 确保环境初始化时创建窗口
        self.model = model
        self.mode = "human"
        if self.model is not None:
            self.mode = "auto"

        
    def run(self):
        running = True
        obs, _ = self.env.reset()
        
        # 初始渲染确保窗口创建
        self.env.render()
        
        while running:
            # 处理事件前检查窗口状态
            if self.env.window is None:
                break
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.mode = "human" if self.mode == "auto" else "auto"
                        print(f"切换到{self.mode}模式")
                    elif self.mode == "human":
                        action = self._key_to_action(event.key)
                        if action is not None:
                            obs, reward, terminated, _, _ = self.env.step(action)
                            if terminated:
                                print("恭喜完成！")
                                obs, _ = self.env.reset()
                                self.env.render()
            
            if self.mode == "auto" and self.model is not None:
                action, _ = self.model.predict(obs)
                obs, reward, terminated, _, _ = self.env.step(action)
                self.env.render()
                if terminated:
                    print("自动模式完成！")
                    obs, _ = self.env.reset()
                    self.env.render()
            
            self.env.render()
        
        self.env.close()

    def _key_to_action(self, key):
        return {
            pygame.K_UP: 2,
            pygame.K_RIGHT: 3,
            pygame.K_DOWN: 0,
            pygame.K_LEFT: 1
        }.get(key, None)

if __name__ == "__main__":
    class RandomModel:
        def predict(self, obs):
            return np.random.randint(4), None
    
    # interface = GameInterface(model=RandomModel())
    interface = GameInterface()
    interface.run()

    # from stable_baselines3 import DQN

    # 训练环境使用非渲染模式
    # train_env = DigitalHuRongEnv(render_mode=None)
    # model = DQN("MlpPolicy", train_env, verbose=1)
    # model.learn(total_timesteps=100000)

    # # 测试时使用渲染模式
    # test_env = DigitalHuRongEnv(render_mode="human")
    # interface = GameInterface(model=model)
    # interface.run()
# Create a custom environment in OpenAI Gym
# https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/

import gymnasium as gym
from gymnasium import spaces

from enum import Enum

from math import factorial
import numpy as np

import pygame


class NPuzzleEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, render_mode=None, size=4):
        self.size = size

        # Observation
        self.observation_space = spaces.Dict(
            {
                "board": spaces.Box(low=0, high=factorial(self.size**2) - 1, dtype=int)
            }
        )

        # State 
        self.board_idx = 0
        self.board_arrangement = self.cantor_inverse_expansion(self.board_idx)

        # Actions
        self.action_space = spaces.Discrete(4) # Action: RIGHT[0], UP[1], LEFT[2], DOWN[3]

        # Render Mode
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None
    
    def _get_obs(self):
        return {
            "board_idx": self.board_idx,
            "board_arrangement": self.board_arrangement
        }
    
    def _get_info(self):
        return {}
    
    def reset(self, seed=None):
        super().reset(seed=seed)

        self.board_idx = self.np_random.integers(0, factorial(self.size**2), size=1, dtype=int)
        self.board_arrangement = self.cantor_inverse_expansion(self.board_idx)

        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    def step(self, action):
        """Action: RIGHT[0], UP[1], LEFT[2], DOWN[3]"""

        # self.size**2 represents the blank space
        blank_idx = self.board_arrangement.index(self.size**2)

        if action == 0: # RIGHT
            if blank_idx % self.size == self.size-1: # blank is at the rightmost position, action is invalid
                target_idx = -1
            else:
                target_idx = blank_idx + 1 

        elif action == 1: # UP
            if blank_idx - self.size < 0: # blank is at the topmost position, action is invalid
                target_idx = -1
            else:
                target_idx = blank_idx - self.size

        elif action == 2: # LEFT
            if blank_idx % self.size == 0: # blank is at the leftmost position, action is invalid
                target_idx = -1
            else:
                target_idx = blank_idx - 1

        elif action == 3:
            if blank_idx + self.size >= self.size**2: # blank is at the bottommost position, action is invalid
                target_idx = -1
            else:
                target_idx = blank_idx + self.size

        # Switch the blank space and the target space
        if target_idx != -1:
            self.board_arrangement[blank_idx], self.board_arrangement[target_idx] = self.board_arrangement[target_idx], self.board_arrangement[blank_idx]
            self.board_idx = self.cantor_expansion(self.board_arrangement)
        


        reward = sum([self.board_arrangement[i]==i for i in range(self.size**2)])
        terminated = reward == self.size**2
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        # print("Current Board:")
        # for i in range(self.size):
        #     print(self.board_arrangement[i*self.size:(i+1)*self.size])
        # print()
        pass
    
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.size*100, self.size*100))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        pix_square_size = 100
        canvas = pygame.Surface((self.size*pix_square_size, self.size*pix_square_size))
        canvas.fill((255, 255, 255))

        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.size*pix_square_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.size*pix_square_size),
                width=3,
            )

        for i in range(self.size):
            for j in range(self.size):
                num = self.board_arrangement[i*self.size+j]
                if num == self.size**2:
                    continue
                pygame.draw.rect(canvas, (0, 0, 0), (j*pix_square_size, i*pix_square_size, pix_square_size, pix_square_size), 1)
                font = pygame.font.Font(None, 36)
                text = font.render(str(num), True, (0, 0, 0))
                canvas.blit(text, (j*pix_square_size+pix_square_size//2-10, i*pix_square_size+pix_square_size//2-10))
        
        self.window.blit(canvas, (0, 0))
        pygame.display.flip()

        self.clock.tick(3)   

    
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            
    def cantor_expansion(self, nums):
        """将排列映射为一个整数"""
        n = self.size**2
        res = 0
        for i in range(n):
            smaller = 0
            for j in range(i+1, n):
                if nums[j] < nums[i]:
                    smaller += 1
            res += smaller * factorial(n-i-1)
        return res

    def cantor_inverse_expansion(self, idx):
        """将一个整数映射为一个排列"""
        n = self.size**2
        idx = int(idx)
        nums = list(range(1, n+1))
        res = []
        idx -= 1  # 索引从0开始
        for i in range(n, 0, -1):
            fact = factorial(i-1)
            cnt = idx // fact
            idx %= fact
            res.append(nums.pop(cnt))
        return res


import gymnasium as gym

from n_puzzle_env import NPuzzleEnv
env = NPuzzleEnv(size=4)

env.reset()
for _ in range(1000):
    env.render()
    observation, reward, terminated, truncated, _ = env.step(env.action_space.sample()) # take a random action
    done = terminated or truncated
    if done:
        env.reset()
env.close()
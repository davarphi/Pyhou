import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv

from stable_baselines3 import PPO

env = PyhouEnv()

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100)

model.save("pyhou")

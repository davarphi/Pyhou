import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
from stable_baselines3 import PPO

env =   FrameSkip(PyhouEnv(render_mode="human"), skip=30)
model = PPO.load('pyhou', env=env)

obs, info = env.reset()
for i in range(1200):
    action, _state = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        obs, info = env.reset()
        break
    # VecEnv resets automatically
    # if done:
    #   obs = vec_env.reset()
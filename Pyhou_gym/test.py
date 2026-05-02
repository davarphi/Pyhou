import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from stable_baselines3 import PPO

env = PyhouEnv(render_mode="human")
model = PPO.load('pyhou', env=env)
print(env.render_mode)
obs, info = env.reset()
for i in range(1200):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        obs, info = env.reset()
    # VecEnv resets automatically
    # if done:
    #   obs = vec_env.reset()
import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
import time

from stable_baselines3 import PPO

reward = {
    "time_penalty": -1,
    "enemy_hit": 10,
    "player_hit": -20,
    "aligned_pos": 200,
    "win":300,
    "loss":-400
}

def print_training_stat(reward_dict):
    print("Stats : ")
    for key, value in reward_dict.items():
        print(f"{key} : {value}")

    time.sleep(1)

env = FrameSkip(PyhouEnv(reward_dict=reward), skip=60)

model = PPO("MlpPolicy", env, verbose=1)
print("Model training begin")
print_training_stat(reward)
model.learn(total_timesteps=10000, callback=InfoCallback())
print("Training finished")

model.save("pyhou")
print("Model saved to pyhou.zip")

import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
import time
import argparse

from stable_baselines3 import PPO

reward = {
    "time_penalty": -0.01,
    "enemy_hit":8,
    "player_hit": -32,
    "aligned_pos": 2,
    "win":50,
    "loss":-200
}

def print_training_stat(reward_dict):
    print(f"Training : {args.pattern}")
    time.sleep(0.5)
    print("Stats : ")
    for key, value in reward_dict.items():
        print(f"{key} : {value}")

    time.sleep(0.5)

parser = argparse.ArgumentParser(description="Training an agent")
parser.add_argument("--pattern", type=str, default="test_attack.json", help="Attack pattern to use")
parser.add_argument("--save", type=str, default="pyhou", help="Saved model name")
args = parser.parse_args()

env = FrameSkip(PyhouEnv(reward_dict=reward, pattern=args.pattern), skip=10)

model = PPO("MlpPolicy", env, verbose=1)
print("Model training begin")
print_training_stat(reward)
model.learn(total_timesteps=100000, callback=InfoCallback())
print("Training finished")

model_name = input(f"Save to {args.save}? [Y/N] :")
if model_name.upper() == "Y":
    model.save(args.save)
    print(f"Model saved to {args.save}.zip")
else:
    print("Model is not saved")

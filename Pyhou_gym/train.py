import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
import time
import argparse
from pathlib import Path

from stable_baselines3 import PPO

# best so far
reward = {
    "time_penalty_early": 0.002,
    "time_penalty_late": -0.01,
    "enemy_hit": 1,
    "player_hit": -1,
    "aligned_shoot": 0.02,
    "prox_penalty": -0.1,
    "win":100,
    "loss":-250
}

def print_training_stat(reward_dict, iter):
    print(f"Training : {args.pattern}")
    time.sleep(0.5)
    print("Stats : ")
    for key, value in reward_dict.items():
        print(f"{key} : {value}")

    print(f"Iteration : {iter}")
    time.sleep(0.5)

parser = argparse.ArgumentParser(description="Training an agent")
parser.add_argument("--pattern", type=str, default="test_attack.json", help="Attack pattern to use")
parser.add_argument("--save", type=str, default="pyhou", help="Saved model name")
parser.add_argument("--iter", type=str, default=500000, help="Training iteration")
args = parser.parse_args()

timestep = int(args.iter)
env = FrameSkip(PyhouEnv(reward_dict=reward, pattern=args.pattern), skip=4)

model = PPO("MlpPolicy", env, verbose=1, ent_coef=0.01)
print("Model training begin")
print_training_stat(reward, timestep)
model.learn(total_timesteps=timestep, callback=InfoCallback())
print("Training finished")

print_training_stat(reward, timestep)
model.save(Path("models") / args.save)
print(f"Model saved to /models/{args.save}.zip")
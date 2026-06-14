import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
from stable_baselines3 import PPO
import time
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="Testing a trained model")
parser.add_argument("--pattern", type=str, default="test_attack.json", help="Attack pattern to use")
parser.add_argument("--model", type=str, default="pyhou", help="Model to use")
args = parser.parse_args()

env = FrameSkip(PyhouEnv(render_mode="human", pattern=args.pattern), skip=10)
model = PPO.load(Path("models") / args.model, env=env)

obs, info = env.reset()

def print_stat():
    health = env.env.game.enemy.health
    bullets_shot = env.env.game.player.bullets_shot
    player_get_hit_count = env.env.game.player.enemy_bullets_hit
    enemy_get_hit_count = env.env.game.player.player_bullets_hit
    time_taken = round(end - start, 3)

    print(f"Bullets that hit player : {player_get_hit_count}")
    print(f"Bullets that hit enemy : {enemy_get_hit_count}")
    print(f"Bullets shot : {bullets_shot}")
    print(f"Enemy health : {health}")
    print(f"Time : {time_taken}")

start = time.time()

for i in range(7200):
    action, _state = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        end = time.time()
        print_stat()
        obs, info = env.reset()
        break
    # VecEnv resets automatically
    # if done:
    #   obs = vec_env.reset()



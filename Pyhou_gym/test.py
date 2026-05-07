import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
from stable_baselines3 import PPO
import time

env = FrameSkip(PyhouEnv(render_mode="human"), skip=10)
model = PPO.load('best', env=env)

obs, info = env.reset()

def print_stat():
    health = env.env.game.enemy.health
    bullets_shot = env.env.game.player.bullets_shot
    player_get_hit_count = env.env.game.player.enemy_bullets_hit
    enemy_get_hit_count = env.env.game.player.player_bullets_hit
    time_taken = round(end - start, 3)

    print(f"Health : {health}")
    print(f"Bullets shot : {bullets_shot}")
    print(f"Bullets that hit enemy : {enemy_get_hit_count}")
    print(f"Bullets that hit player : {player_get_hit_count}")
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



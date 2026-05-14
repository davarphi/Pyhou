import gymnasium as gym
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from pyhou_gym_env.wrappers import FrameSkip, InfoCallback
from stable_baselines3 import PPO

env =   FrameSkip(PyhouEnv(render_mode="human"), skip=10)
model = PPO.load('bestsofar', env=env)

obs, info = env.reset()
for i in range(7200):
    action, _state = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        obs, info = env.reset()
        break
    # VecEnv resets automatically
    # if done:
    #   obs = vec_env.reset()


# health = env.game.enemy.health
# bullets_shot = env.game.player.bullets_shot
# player_got_hit_count  = env.game.player.enemy_bullets_hit
# enemy_got_hit_count = env.game.player.player_bullets_hit

# print(f"Enemy_health : {health}")
# print(f"Bullets_shot : {bullets_shot}")
# print(f"Bullets_that_hit_player : {player_got_hit_count}")
# print(f"Bullets_that_hit_enemy {enemy_got_hit_count}")
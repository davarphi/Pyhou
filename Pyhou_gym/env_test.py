from gymnasium.utils.env_checker import check_env
from pyhou_gym_env.envs.pyhou_gym import PyhouEnv
from gymnasium import register, make

register(
    id="Pyhou-v0",
    entry_point="pyhou_gym_env.envs.pyhou_gym:PyhouEnv",
)

env = make("Pyhou-v0")
env = PyhouEnv()
check_env(env)
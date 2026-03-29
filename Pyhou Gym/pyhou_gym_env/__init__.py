from gymnasium.envs.registration import register

register(
    id="pyhou_gym_env/Pyhou-v0",
    entry_point="pyhou_gym_env.envs:PyhouEnv",
)

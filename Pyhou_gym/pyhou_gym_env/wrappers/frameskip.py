import gymnasium as gym

class FrameSkip(gym.Wrapper):
    def __init__(self, env, skip=4):
        super().__init__(env)
        self.skip = skip

    def step(self, action):
        total_reward = 0.0
        terminated = truncated = False
        obs = None
        for i in range(self.skip):
            self.env.unwrapped.build_obs = (i == self.skip - 1)   # full obs only on last frame
            obs, reward, terminated, truncated, info = self.env.step(action)
            total_reward += reward
            if (terminated or truncated):
                if not (self.env.unwrapped.build_obs):
                    obs = self.env.unwrapped._get_obs()
                break
            
        return obs, total_reward, terminated, truncated, info
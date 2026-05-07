from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from pygame.math import Vector2
from components.game_logic import Game
from pathlib import Path

class PyhouEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    # Here
    def __init__(self, render_mode=None, reward_dict={}):
        # Pygame size
        self.WIDTH = 576
        self.HEIGHT = 672
        self.reward = reward_dict

        json_path = Path(__file__).parent.parent.parent / "attacks"/ "hard.json" # Ini nanti ganti
        self.game = Game(str(json_path))
        # self.game = Game("test_attack.json")
        """ Take 1 : Reasonable Human Obs
        Player pos -> 2
        Enemy pos -> 2
        Enemy proj : Take 10 nearest for now, take pos (2) and dir vel (2) and speed -> 5*10 = 50 
        Total = 54
        """
        self.observation_space = spaces.Box(low=-1, high=1, shape=(54,), dtype=np.float32)
        # ^ I really don't know what to put...

        # We have 9 x 2 x 2 actions, corresponding to the 8 cardinal directions + 1 stay, Binary slow mode, Binary shoot
        self.action_space = spaces.MultiDiscrete([9, 2, 2])


        """
        v Haven't implemented rendering bruh
        """
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    
    def _get_obs(self):
        # -1 is better value for missing values though
        obs = np.zeros(54, dtype=np.float32)

        obs[0] = self.game.player.pos.x / self.WIDTH # Player rel x pos
        obs[1] = self.game.player.pos.y / self.HEIGHT # Player rel y pos
        obs[2] = self.game.enemy.pos.x / self.WIDTH # Enemy rel x pos
        obs[3] = self.game.enemy.pos.y / self.HEIGHT # Enemy rel y pos

        proj_list = self.game.enemy.bullets
        nearest = sorted(proj_list, key=lambda p : ((p.pos.x - self.game.player.pos.x)**2 + (p.pos.y - self.game.player.pos.y)**2))[:10]

        for i, p in enumerate(nearest):
            obs[5*i + 4] = p.pos.x / self.WIDTH
            obs[5*i + 5] = p.pos.y / self.HEIGHT 
            obs[5*i + 6] = p.vel.x / p.speed
            obs[5*i + 7] = p.vel.y / p.speed
            obs[5*i + 8] = np.tanh(min(p.speed / 25, 50)) # 25 is kinda mid-ish

        return obs 
        # Return the 54-vector array of the observation

    def _get_info(self):
        health = self.game.enemy.health
        bullets_shot = self.game.player.bullets_shot
        player_got_hit_count  = self.game.player.enemy_bullets_hit
        enemy_got_hit_count = self.game.player.player_bullets_hit

        return {"Enemy_health" : health, 
                "Bullets_shot" : bullets_shot,
                "Bullets_that_hit_player" : player_got_hit_count,
                "Bullets_that_hit_enemy" : enemy_got_hit_count}
        # This is for now
        # Should be the endgame stats

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.game.reset()

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        """
        Alpha stage rewards : 
        -0.0015 (30/18000) per step penalty. (chaneg is TIME_LIMIT is changed)
        +1 per enemy_hits
        -0.5 per player_hits
        +100 per win
        -150 per loss
        """
        prev_player_bullets_hit = self.game.player.player_bullets_hit
        prev_enemy_bullets_hit = self.game.player.enemy_bullets_hit
        self.game.apply_step(action)
        terminated = self.game.is_terminated()
        truncated = self.game.is_truncated() # Replace this to False to use the built-in TimeLimit wrapper
        reward = 0 

        reward += self.reward.get("time_penalty", -0.001)

        enemy_hits = self.game.player.player_bullets_hit - prev_player_bullets_hit
        player_hits = self.game.player.enemy_bullets_hit - prev_enemy_bullets_hit

        in_range = np.abs(self.game.player.pos.x - self.game.enemy.pos.x) / self.game.player.pos.distance_to(self.game.enemy.pos) <= np.sin(np.deg2rad(2))
        shootable = self.game.player.pos.y > self.game.enemy.pos.y

        if (in_range and shootable):
            reward += self.reward.get("aligned_pos", 0)

        reward += enemy_hits * self.reward.get("enemy_hit", 1)
        reward += player_hits * self.reward.get("player_hit", -0.5)


        if self.game.is_win():
            reward += self.reward.get("win", 100)

        elif self.game.is_loss():
            reward += self.reward.get("loss", 150)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, truncated, info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        elif self.render_mode == "human":
            self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.WIDTH, self.HEIGHT))
        canvas.fill((128, 128, 128))

        # Draw the stuff here
        player = self.game.player
        enemy = self.game.enemy
        pygame.draw.circle(canvas, (0, 0, 128), (player.pos.x, player.pos.y), player.r)
        pygame.draw.circle(canvas, (128, 0, 0), (enemy.pos.x, enemy.pos.y), enemy.r)
        pygame.draw.circle(canvas, (0, 0, 0), (enemy.pos.x, enemy.pos.y), enemy.r, 1)

        for proj in player.bullets:
            pygame.draw.circle(canvas, (128, 0, 0, 50), (proj.pos.x, proj.pos.y), proj.r)
            pygame.draw.circle(canvas, (0,0,0,50), (proj.pos.x, proj.pos.y), proj.r, 1)

        for proj in enemy.bullets:
            pygame.draw.circle(canvas, (255, 255, 255, 50), (proj.pos.x, proj.pos.y), proj.r)
            pygame.draw.circle(canvas, (0, 0, 128, 50), (proj.pos.x, proj.pos.y), proj.r, 2)

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to
            # keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

if __name__ == "__main__":
    print("Success")
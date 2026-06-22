from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from pygame.math import Vector2
import math
from components.game_logic import Game
from components.constants import *
from pathlib import Path


D_SCALE = 40.0
T_SCALE = 30.0
NUM_SECTORS = 8
N_IMMINENT = 3
MAX_BULLET_SPEED = 40.0
MAX_PLAYER_SPEED = 5.0
D_REF = 200.0
T_CAP = 120.0
PROX_CAP = 4.0
SIGMA = math.radians(6)
OBS_SIZE = 46 # Normal = 9 + 8 + 21 = 38 atau 9 + 8 = 17 (minus imminent bullet) atau 9 + 16 + 21 = 46(Waktu imminence) 
TIME_LIMIT = 7200

def cpa(bullet, player):
    pos_vec = bullet.pos - player.pos

    rv = pos_vec * bullet.vel

    if rv >= 0:
        return math.inf, pos_vec.length(), 0.0
    
    vv = bullet.vel.length_squared()

    if vv < 1e-8:
        return math.inf, pos_vec.length(), 0.0
    
    t = - rv/vv
    d_min_vec = pos_vec + bullet.vel*t
    d_min = d_min_vec.length()
    threat = math.exp(-d_min / D_SCALE) * math.exp(-t / T_SCALE)
    return t, d_min, threat

def sector_of(pos_vec):
    ang = math.atan2(pos_vec.y, pos_vec.x)
    return int(round(ang / (2 * math.pi / NUM_SECTORS))) % NUM_SECTORS

def get_angle_pos(enemy, player):
    dx = enemy.pos.x - player.pos.x
    dy = player.pos.y - enemy.pos.y # in y coord, down is positive
    angle_pos = math.atan2(dx, dy)

    return angle_pos 


class PyhouEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    # Here
    def __init__(self, render_mode=None, reward_dict={}, pattern="test_attack.json", iter=500000):
        # Pygame size
        self.WIDTH = 576
        self.HEIGHT = 672
        self.reward = reward_dict
        self.iter = iter

        json_path = Path(__file__).parent.parent.parent / "attacks"/ pattern # Ini nanti ganti
        self.game = Game(str(json_path))
        """ Take 1 : Reasonable Human Obs
        Player pos -> 2
        Enemy pos -> 2
        Enemy proj : Take 10 nearest for now, take pos (2) and dir vel (2) and speed -> 5*10 = 50 
        Total = 54
        """
        self.observation_space = spaces.Box(low=-1, high=1, shape=(OBS_SIZE,), dtype=np.float32)
        self._placeholder = np.zeros(OBS_SIZE, dtype=np.float32)
        # ^ I really don't know what to put...

        # We have 9 x 2 x 2 actions, corresponding to the 8 cardinal directions + 1 stay, Binary slow mode, Binary shoot
        self.action_space = spaces.MultiDiscrete([9, 2, 2])


        """
        v Haven't implemented rendering bruh
        """
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.build_obs = True

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

        self.prev_angle = None
    
    def _get_danger(self):
        d = 0.0
        for b in self.game.enemy.bullets:
            _, _, th = cpa(b, self.game.player)
            if th > d:
                d = th
        return d
    
    def _get_obs(self):
        obs = np.zeros(OBS_SIZE, dtype=np.float32)
        dx = self.game.enemy.pos.x - self.game.player.pos.x
        dy = self.game.player.pos.y - self.game.enemy.pos.y # in y coord, down is positive
        angle_pos = math.atan2(dx, dy) 
        player_vel = self.game.player.vel * self.game.player.speed

        obs[0] = self.game.player.pos.x / self.WIDTH # Player rel x pos
        obs[1] = self.game.player.pos.y / self.HEIGHT # Player rel y pos
        obs[2] = dx / self.WIDTH 
        obs[3] = dy / self.HEIGHT
        obs[4] = player_vel.x / MAX_PLAYER_SPEED
        obs[5] = player_vel.y / MAX_PLAYER_SPEED
        obs[5] = 1.0 if self.game.player.is_slow else 0.0 
        obs[7] = angle_pos / (math.pi) 
        obs[8] = (TIME_LIMIT - self.game.tick)/TIME_LIMIT

        sector_threat = [0.0] * NUM_SECTORS
        time_imminence = [0.0] * NUM_SECTORS
        cache = []

        for b in self.game.enemy.bullets:
            t, d_min, threat = cpa(b, self.game.player)
            if threat <= 0.0:
                continue

            pos_vec = b.pos - self.game.player.pos
            s = sector_of(pos_vec)
            sector_threat[s] = max(sector_threat[s], threat)
            time_imminence[s] = 1.0 - min(t, T_CAP) / T_CAP
            cache.append((threat, t, d_min, pos_vec, b))

        
        # for j in range(NUM_SECTORS):
        #     n = 9 + j
        #     obs[n] = sector_threat[j]


        for j in range(NUM_SECTORS):
            n = 9 + 2 * j
            obs[n] = sector_threat[j]
            obs[n + 1] = time_imminence[j]

        
        cache.sort(key=lambda c: c[0], reverse=True)
        for i in range(N_IMMINENT):
            n = 25 + i * 7 # 17 <-> 25
            if i < len(cache):
                _, t, d_min, pos_vec, b = cache[i]
                obs[n + 0] = pos_vec.x / self.WIDTH
                obs[n + 1] = pos_vec.y / self.HEIGHT
                obs[n + 2] = b.vel.x / MAX_BULLET_SPEED
                obs[n + 3] = b.vel.y / MAX_BULLET_SPEED
                obs[n + 4] = min(t, T_CAP) / T_CAP
                obs[n + 5] = min(d_min, D_REF) / D_REF
                obs[n + 6] = 1.0    # presence bit

        return obs 
        #Return the -vector array of the observation

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
        to_enemy = self.game.enemy.pos - self.game.player.pos
        self.prev_angle = abs(to_enemy.angle_to(pygame.math.Vector2(0, 1))) 
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self, action):
        prev_player_bullets_hit = self.game.player.player_bullets_hit
        prev_enemy_bullets_hit = self.game.player.enemy_bullets_hit

        self.game.apply_step(action)
        terminated = self.game.is_terminated()
        truncated = self.game.is_truncated() # Replace this to False to use the built-in TimeLimit wrapper
        reward = 0.0
        if self.game.tick < self.iter // 4:
            reward += self.reward.get("time_penalty_early", 0.0) # time_penalty at first
        else:
            reward += self.reward.get("time_penalty_late", 0.0) 
        #Bullet hits related
        enemy_hits = self.game.player.player_bullets_hit - prev_player_bullets_hit
        player_hits = self.game.player.enemy_bullets_hit - prev_enemy_bullets_hit

        reward += enemy_hits * self.reward.get("enemy_hit", 0.0)
        reward += player_hits * self.reward.get("player_hit", 0.0)

        if self.game.is_win():
            reward += self.reward.get("win", 0.0)
        elif self.game.is_loss():
            reward += self.reward.get("loss", 0.0)

        if getattr(self, "build_obs", True):
            observation = self._get_obs()
        else:
            observation = self._placeholder

        info = self._get_info()

        danger = self._get_danger()
        gate = 1 - danger
        prox = danger

        # proximity penalty
        reward += prox * self.reward.get("prox_reward", 0.0)

       
        if action[2] == 1:
            angle = get_angle_pos(self.game.enemy, self.game.player)
            aligned = math.exp(-(angle / SIGMA) ** 2)
            reward += gate * aligned * self.reward.get("aligned_shoot", 0.0)

        
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
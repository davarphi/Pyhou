from .player import Player
from .enemy import Enemy
from .constants import *
from pygame.math import Vector2


DIRECTIONAL_VECTOR = {
    0: (-1, 1),
    1: (0, 1),
    2: (1, 1),
    3: (-1, 0),
    4: (0, 0),
    5: (1, 0),
    6: (-1, -1),
    7: (0, -1), 
    8: (1, -1)
}

TIME_LIMIT = 2400

class Game:
    def __init__(self, attack_pat):
        self.width = WIDTH
        self.height = HEIGHT
        self.attack_pat = attack_pat
        self.reset()
        
    def reset(self):
        self.player = Player(WIDTH//2, HEIGHT//2)
        self.enemy = Enemy(WIDTH/2, 40, self.attack_pat)
        self.tick = 0
        self.done = False
        self.is_player_touch_enemy = False
        self.time_finish = 0


    def apply_step(self, action):
        vel_dir = DIRECTIONAL_VECTOR[action[0]]
        self.player.vel = Vector2(vel_dir)
        is_slow = action[1] == 1
        is_shoot = action[2] == 1

        if is_shoot:
            self.player.shoot(is_slow)
        
        self.player.update_pos(is_slow)
        self.player.update_proj()
        self.enemy.update_action(self.player.pos)
        self.enemy.update_proj()
        self.check_enemy_collisions()
        self.check_player_collisions()

        self.tick += 1

    def is_game_done(self):
        return (
            self.is_terminated() or
            self.is_truncated()
        )
    
    def is_terminated(self):
        return (
            self.is_win() or
            self.is_loss()
        )
    
    def is_win(self):
        return self.enemy.health <= 0
    
    def is_loss(self):
        enemy_to_player_dist = self.enemy.pos.distance_to(self.player.pos)
        return enemy_to_player_dist < self.player.r + self.enemy.r

    def is_truncated(self):
        return (self.tick >= TIME_LIMIT)

    def check_player_collisions(self):
        for bullet in self.enemy.bullets[:]:
            if self._is_bullet_hit(bullet, self.player):
                bullet.is_remove = True
                self.player.enemy_bullets_hit += 1

    def check_enemy_collisions(self):
        for bullet in self.player.bullets[:]:
            if self._is_bullet_hit(bullet, self.enemy):
                bullet.is_remove = True
                self.player.player_bullets_hit += 1
                self.enemy.take_damage()

    @staticmethod
    def _is_bullet_hit(bullet, object):
        distance = bullet.pos.distance_to(object.pos)
        return (distance < bullet.r + object.r)
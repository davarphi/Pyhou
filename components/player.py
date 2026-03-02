import pygame
from pygame.math import Vector2
from math import radians, pi
from .projectile import Projectile

class Player:
    bound_w = 576
    bound_h = 672
    
    def __init__(self, pos_x, pos_y):
        self.BASE_SPEED = 5
        self.DEFAULT_POS = Vector2(Player.bound_w/2 + Player.bound_h/2)

        self.pos = Vector2(pos_x, pos_y)
        self.vel = Vector2(0,0)
        self.r = 7
        self.bullets = []
        self.cooldown_time = 10
        self.shot_cooldown = 0

        self.bullets_hit = 0

    def update_pos(self, player_input):
        self.vel.x = player_input["right"] - player_input["left"]
        self.vel.y = player_input["down"] - player_input["up"]

        speed = self.BASE_SPEED if not(player_input["slow"]) else self.BASE_SPEED/2

        if self.vel !=Vector2(0,0):
            self.pos += Vector2.normalize(self.vel)*speed

        if (self.pos.x < self.r): 
            self.pos.x = self.r
        elif (self.pos.x > self.bound_w - self.r): 
            self.pos.x = self.bound_w - self.r

        if (self.pos.y < self.r): 
            self.pos.y = self.r
        elif (self.pos.y > self.bound_h - self.r): 
            self.pos.y = self.bound_h - self.r
    
    def draw(self, window):
        pygame.draw.circle(window, (128, 0, 0), (self.pos.x, self.pos.y), self.r)
        pygame.draw.circle(window, (0, 0, 0), (self.pos.x, self.pos.y), self.r, 1)

        for bullet in self.bullets:
            bullet.draw(window)

    def shoot(self, player_state):
        if (player_state["slow"]):
            attack_degs = [pi/2-radians(2), pi/2, pi/2+radians(2)]
        else:
            attack_degs = [pi/2-radians(4), pi/2, pi/2+radians(4)]
        
        if self.shot_cooldown == 0:
            for angle in attack_degs:
                bullet = Projectile(self.pos.x, self.pos.y + self.r // 2, angle)
                self.bullets.append(bullet)

            self.shot_cooldown = self.cooldown_time

    def update_proj(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_bound():
                bullet.is_remove = True

            if bullet.is_remove:
                self.bullets.remove(bullet)

            


    









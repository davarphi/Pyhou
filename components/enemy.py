import pygame
from math import atan2, radians, degrees
from pygame.math import Vector2
from .action import Action
import json
from .attack_pattern import *
from .constants import *
import os

class Enemy:
    def __init__(self, pos_x, pos_y, pattern_file):
        self.pos = Vector2(pos_x, pos_y)
        self.vel = Vector2(0, 0)
        self.speed = 0
        self.r = 14
        self.health = 100.0
        self.bullets = []

        path = os.path.join("attacks", pattern_file) 
        with open(path, "r") as f:
            self.actions_data = json.load(f)
        self.current_action = None
        
        self.start_action()
    
    def take_damage(self):
        if self.health > 0:
            self.health -= DAMAGE
        print(self.health) # Remove this later

    def start_action(self):
        self.current_action = Action(self.actions_data)

    def shoot(self, step, player_pos):
        pattern_name = step.get("pattern")
        valid_name = ["fan_aim", "fan_no_aim", "ring_hit_aim", \
                      "ring_no_hit_aim", "ring_no_hit_aim", "ring_no_hit_no_aim", \
                      "fan_random", "ring_random", "meek_random"]
        if pattern_name in valid_name:
            new_projectiles = self.get_projectile(pattern_name, step, player_pos)
        
        self.bullets.extend(new_projectiles)

    def get_projectile(self, pattern_name, step, player_pos):
        new_projectile = []
        cnt1 = step.get("cnt1")
        cnt2 = step.get("cnt2")
        ang1 = step.get("ang1")
        ang2 = step.get("ang2")
        spe1 = step.get("spe1")
        spe2 = step.get("spe2")
        player_angle_rad = atan2(-(player_pos.y - self.pos.y), player_pos.x - self.pos.x)
        player_angle = degrees(player_angle_rad)

        match pattern_name:
            case "fan_aim":
                new_projectile = get_fan_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos, player_angle)
            case "fan_no_aim":
                new_projectile = get_fan_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos, 0)
            case "ring_hit_aim":
                new_projectile = get_ring_hit_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos, player_angle)
            case "ring_hit_no_aim":
                new_projectile = get_ring_hit_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos, 0)
            case "ring_no_hit_aim":
                new_projectile = get_ring_no_hit_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos, player_angle)
            case "ring_no_hit_no_aim":
                new_projectile = get_ring_no_hit_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos, 0)
            case "fan_random":
                new_projectile = get_fan_random_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos)
            case "ring_random":
                new_projectile = get_ring_random_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos)
            case "meek_random":
                new_projectile = get_meek_random_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, self.pos)

                
        return new_projectile
    
    #Utlity function
    def update_action(self, player_pos):
        if self.current_action is not None:
            self.current_action.update(self, player_pos)

            if self.current_action.completed:
                self.current_action = None
    
    def update_pos(self, step):
        self.vel = Vector2(step.get("vel_x"), step.get("vel_y"))
        self.speed = step.get("speed")
        self.pos += self.vel*self.speed

    def update_proj(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_bound():
                bullet.is_remove = True

            if bullet.is_remove:
                self.bullets.remove(bullet)


     
            


    









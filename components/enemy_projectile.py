import math
import pygame
from pygame.math import Vector2
from math import cos, sin, pi
from .constants import *

class EnemyProjectile():
    bound_w = WIDTH
    bound_h = HEIGHT

    def __init__(self, pos_x, pos_y, angle, speed):
        self.start = Vector2(pos_x, pos_y)
        self.pos = Vector2(pos_x, pos_y)
        self.speed = speed
        self.vel = Vector2(cos(angle), -sin(angle))*self.speed
        self.r = 5
        self.is_remove = False
    
    def update(self):
        self.pos += self.vel
    
    # def draw(self, window):
    #     # Need to change
    #     pygame.draw.circle(window, (255, 255, 255, 50), (self.pos.x, self.pos.y), self.r)
    #     pygame.draw.circle(window, (0, 0, 128, 50), (self.pos.x, self.pos.y), self.r, 2)

    def is_out_bound(self):
        return (self.pos.y < -self.r/2 or 
                self.pos.y > self.bound_h + self.r/2 or 
                self.pos.x < -self.r/2 or 
                self.pos.x > self.bound_w + self.r/2)





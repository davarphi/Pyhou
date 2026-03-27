from components.player import Player
from components.enemy import Enemy
from components.constants import *
from pygame.math import Vector2
from math import radians, pi

class GameLogic:
    def __init__(self, attack_pat):
        self.player = Player(WIDTH//2, HEIGHT//2)
        self.enemy = Enemy(WIDTH/2, 40, attack_pat)
        self.tick = 0
        self.done = False

    def reset():
        pass
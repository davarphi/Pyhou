import pygame
from components.player import Player
from components.enemy import Enemy
from components.constants import *

pygame.init()


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Size comp")

player = Player(100, 100)
player2 = Player(120, 100)

running = True

def draw_player(window, player):
    pygame.draw.circle(window, (128, 0, 0), (player.pos.x, player.pos.y), player.r)
    pygame.draw.circle(window, (0, 0, 0), (player.pos.x, player.pos.y), player.r, 1)

while running:
    WINDOW.fill((128, 128, 128))

    draw_player(WINDOW, player)
    draw_player(WINDOW, player2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

    pygame.display.update()

pygame.quit()
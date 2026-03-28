import pygame
from components.player import Player
from components.enemy import Enemy
from components.constants import *
from game_logic import Game
import argparse


parser = argparse.ArgumentParser(description="Pyhou")
parser.add_argument("--pattern", type=str, default="test_attack.json", help="Attack pattern to use")
args = parser.parse_args()

DIRECTION_MAP = {
    (-1, 1): 0,
    (0, 1): 1,
    (1, 1): 2,
    (-1, 0): 3,
    (0, 0): 4,
    (1, 0): 5,
    (-1, -1): 6,
    (0, -1): 7, 
    (1, -1): 8
}

pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pyhou")

CLOCK = pygame.time.Clock()

game = Game(args.pattern)

def get_action_from_input(keys):
    action = [4, 0, 0]

    x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    action[0] = DIRECTION_MAP[(x, y)]

    if keys[pygame.K_LSHIFT]:
        action[1] = 1
    if keys[pygame.K_z]:
        action[2] = 1

    return action

def draw_player(window, player):
    pygame.draw.circle(window, (128, 0, 0), (player.pos.x, player.pos.y), player.r)
    pygame.draw.circle(window, (0, 0, 0), (player.pos.x, player.pos.y), player.r, 1)

    for proj in player.bullets:
        draw_player_proj(window, proj)

def draw_player_proj(window, proj):
    pygame.draw.circle(window, (128, 0, 0, 50), (proj.pos.x, proj.pos.y), proj.r)
    pygame.draw.circle(window, (0,0,0,50), (proj.pos.x, proj.pos.y), proj.r, 1)

def draw_enemy(window, enemy):
    pygame.draw.circle(window, (0, 128, 128), (enemy.pos.x, enemy.pos.y), enemy.r)
    pygame.draw.circle(window, (0, 0, 0), (enemy.pos.x, enemy.pos.y), enemy.r, 1) 

    for proj in enemy.bullets:
        draw_enemy_proj(window, proj)

def draw_enemy_proj(window, proj):
    pygame.draw.circle(window, (255, 255, 255, 50), (proj.pos.x, proj.pos.y), proj.r)
    pygame.draw.circle(window, (0, 0, 128, 50), (proj.pos.x, proj.pos.y), proj.r, 2)

while not game.is_game_done():
    WINDOW.fill((128, 128, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    action = get_action_from_input(keys)

    game.apply_step(action)
    draw_player(WINDOW, game.player)
    draw_enemy(WINDOW, game.enemy)
    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()

if game.is_player_touch_enemy:
    print("Player hit the enemy!")

print(f"Bullets shot : {game.player.bullets_shot}")

if game.player.bullets_shot == 0:
    game.player.bullets_shot = 1

accuracy = game.player.player_bullets_hit/game.player.bullets_shot
print(f"Accuracy : {accuracy:.3f}")
print(f"Enemy bullets hit : {game.player.enemy_bullets_hit}")
print(f"Time finished: {game.tick/60:2f} s")

if game.enemy.health > 0:
    print(f"Enemy last health : {game.enemy.health}")
else:
    print("Enemy defeated!")
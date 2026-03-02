import pygame
from components.player import Player
from components.enemy import Enemy
import os

pygame.init()

WINDOW = pygame.display.set_mode((576, 672))
pygame.display.set_caption("Pyhou")

CLOCK = pygame.time.Clock()
running = True

player = Player(WINDOW.get_width()/2, WINDOW.get_height()/2)
enemy = Enemy(WINDOW.get_width()/2, 40)
player_input = {"left":False, "right":False, "up":False, "down":False, "slow":False, "shoot":False}
is_player_touch_enemy = False

def check_input(key, value):
    if key == pygame.K_LEFT:
        player_input["left"] = value
    elif key == pygame.K_UP:
        player_input["up"] = value
    elif key == pygame.K_DOWN:
        player_input["down"] = value
    elif key == pygame.K_RIGHT:
        player_input["right"] = value
    elif key == pygame.K_LSHIFT:
        player_input["slow"] = value
    elif key == pygame.K_z:
        player_input["shoot"] = value

def check_player_collisions():
    for bullet in enemy.bullets[:]:
        if is_bullet_hit(bullet, player):
            bullet.is_remove = True
            player.bullets_hit += 1

def check_enemy_collisions():
    for bullet in player.bullets[:]:
        if is_bullet_hit(bullet, enemy):
            bullet.is_remove = True
            enemy.take_damage()

def is_bullet_hit(bullet, object):
    distance = bullet.pos.distance_to(object.pos)
    return (distance < bullet.r + object.r)

while running:
    WINDOW.fill((128, 128, 128))
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            check_input(event.key, True)
        elif event.type == pygame.KEYUP:
            check_input(event.key, False)
            
    if (player_input["shoot"]):
        player.shoot(player_input)

    player.update_pos(player_input)
    player.update_proj()
    enemy.update_action(player.pos)
    enemy.update_proj()
    check_enemy_collisions()
    check_player_collisions()
    player.draw(WINDOW)
    enemy.draw(WINDOW)
    enemy_to_player_dist = enemy.pos.distance_to(player.pos)
    if (enemy_to_player_dist < player.r + enemy.r):
        is_player_touch_enemy = True
        time_finish = pygame.time.get_ticks()
        running = False
    elif (enemy.health <= 0):
        time_finish = pygame.time.get_ticks()
        running = False
    pygame.display.update()

pygame.quit()

if is_player_touch_enemy:
    print("Player hit the enemy!")
print(f"Bullets hit : {player.bullets_hit}")
print(f"Time finished: {time_finish/1000} s")
if enemy.health > 0:
    print(f"Enemy last health : {enemy.health}")
else:
    print("Enemy defeated!")
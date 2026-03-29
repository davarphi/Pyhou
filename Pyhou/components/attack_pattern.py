from math import radians, pi, sin, cos
from pygame.math import Vector2
from .enemy_projectile import EnemyProjectile
from random import randint, random

# Make bullets with all the need speed & angle
def get_fan_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, pos=Vector2(0,0), rel_with=0):
    new_projectile = []
    for i in range(cnt2):
        if cnt2 == 1:
            speed = spe1
        else:
            speed = spe1 - i*(spe1 - spe2)/(cnt2 - 1)
        for j in range(cnt1):
                angle = rel_with - ang1 + ang2*(-(cnt1-1)/2 + j)
                bullet = EnemyProjectile(pos.x, pos.y, radians(angle), speed)
                new_projectile.append(bullet)

    return new_projectile

def get_ring_hit_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, pos=Vector2(0,0), rel_with=0):
    new_projectile = []
    for i in range(cnt2):
        if cnt2 == 1:
            speed = spe1
        else:
            speed = spe1 - i*(spe1 - spe2)/(cnt2 - 1)
        for j in range(cnt1):
            angle = rel_with - ang1 + (360/cnt1)*j - ang2*i
            bullet = EnemyProjectile(pos.x, pos.y, radians(angle), speed)
            new_projectile.append(bullet)

    return new_projectile

def get_ring_no_hit_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, pos=Vector2(0,0), rel_with=0):
    new_projectile = []
    for i in range(cnt2):
        if cnt2 == 1:
            speed = spe1
        else:
            speed = spe1 - i*(spe1 - spe2)/(cnt2 - 1)
        for j in range(cnt1):
            angle = rel_with - ang1 + (360/cnt1)*(j+0.5) - ang2*i
            bullet = EnemyProjectile(pos.x, pos.y, radians(angle), speed)
            new_projectile.append(bullet)

    return new_projectile

def get_fan_random_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, pos):
    new_projectile = []
    for i in range(cnt2):
        if cnt2 == 1:
            speed = spe1
        else:
            speed = spe1 - i*(spe1 - spe2)/(cnt2 - 1)
        for j in range(cnt1):
                random_offset = -ang2 + round(random()*2*ang2, 3)
                angle = ang1 + random_offset
                bullet = EnemyProjectile(pos.x, pos.y, radians(angle), speed)
                new_projectile.append(bullet)

    return new_projectile

def get_ring_random_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, pos=Vector2(0,0)):
    new_projectile = []
    for i in range(cnt2):
        for j in range(cnt1):
            speed = round(spe1 + random()*spe2)
            angle = - ang1 + (360/cnt1)*j - ang2*i
            bullet = EnemyProjectile(pos.x, pos.y, radians(angle), speed)
            new_projectile.append(bullet)

    return new_projectile

def get_meek_random_pattern_bullets(cnt1, cnt2, ang1, ang2, spe1, spe2, pos=Vector2(0,0)):
    new_projectile = []
    for i in range(cnt2):
        for j in range(cnt1):
            speed = round(spe1 + random()*spe2, 3)
            random_offset = -ang2 + round(random()*2*ang2, 3)
            angle = ang1 + random_offset
            bullet = EnemyProjectile(pos.x, pos.y, radians(angle), speed)
            new_projectile.append(bullet)

    return new_projectile
     
if __name__ == "__main__":
    output = get_fan_pattern_bullets(7, 3, 0, 5, 6, 2)

    for i in output:
         print(i)
import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

#from PLAYER_IMAGES import PLAYER_IMAGES

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDHT = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0, 0, 0,)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDHT,HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDHT, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load('player.png').convert_alpha() #pygame.Surface(player_size)
player_size = player.get_size()
#player.fill(COLOR_BLACK)
player_rect = player.get_rect().move((0, 300))
player_move_down = [0, 1]
player_move_right = [1, 0]
player_move_top = [0, -1]
player_move_left = [-1, 0]

def create_enemy():
    enemy =pygame.image.load('enemy.png').convert_alpha() #pygame.Surface(enemy_size)
    enemy_size = enemy.get_size()
    #enemy.fill((COLOR_BLUE))
    enemy_rect = pygame.Rect(1100, random.randint(0, HEIGHT), *enemy_size)
    enemy_move =  [random.randint(-6, -1) ,0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus =pygame.image.load('bonus.png').convert_alpha()  #pygame.Surface(bonus_size)
    bonus_size = bonus.get_size()
    #bonus.fill((COLOR_RED))
    bonus_rect = pygame.Rect(random.randint(300, WIDHT), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 4)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True

while playing:
    FPS.tick(120)
            
    for event in pygame.event.get():
        if event.type == QUIT:
            plaing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
        if image_index >= len(PLAYER_IMAGES):
            image_index = 0
            
    #main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move
    
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
        
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
    
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
        
    if keys[K_RIGHT] and player_rect.right < WIDHT:
        player_rect = player_rect.move(player_move_right)
        
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_top)
        
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
            
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
        if player_rect.colliderect(enemy[1]):
            playing = False
         
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDHT-50, 20))   
    main_display.blit(player, player_rect)
    
    pygame.display.flip()
    
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
   
    
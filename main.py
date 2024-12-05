import pygame
import os
from pygame import mixer
from GameClass import Game
from PlayerClass import Player
from EnemyClass import Enemy
from DrawingClass import Drawing

BACKGROUND = pygame.image.load(os.path.join('img', 'background.png'))
ICON_IMAGE = pygame.image.load(os.path.join('img', 'title_icon.png'))
PLAYER_IMAGE = pygame.image.load(os.path.join('img', 'player_image.png'))
TITLE = 'Space Invaders Hybridge'
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(TITLE)

pygame.init()
try:
    mixer.music.load('sounds/background_song.mp3')
    
except:
    print("No se pudo cargar el sonido")
    pass

def main():
    run = True
    clock = pygame.time.Clock()
    FPS = 60

    try:
        mixer.music.play(-1)
    except:
        pass

    font = pygame.font.SysFont('comicsans', 50)
    game = Game(font, FPS, 3, WIN, WIDTH, HEIGHT, 0, clock)
    player_x = ((WIDTH)-(PLAYER_IMAGE.get_width())) / 2
    player_y = 480
    player = Player(x=player_x, y=player_y, x_speed=5, y_speed=4)
    enemy_init = Enemy(speed=0.8)
    enemy_wave = 4
    enemies = enemy_init.create(enemy_wave)
    draw = Drawing(WIN)
    draw.drawing(game, player, enemies, FPS=60)

    while run:
        clock.tick(FPS)
        if game.over():
            run = False
            continue

        if game.escape():
            run = False
            continue

        if len(enemies) == 0:
            game.level += 1
            enemy_wave += 1
            enemy_init.increase_speed()
            player.increase_speed()
            enemies = enemy_init.create(amount=enemy_wave)
            new_level = True

        if game.level % 3 == 0 and new_level:
            if player.max_amount_bullets < 10:
                player.max_amount_bullets += 1
            if game.lives < 6:
                game.lives += 1
            new_level = False

        player.move()
        player.create_bullets()
        game.reload_bullet(len(player.bullets))
        player.cooldown()

        for enemy in enemies:
            enemy.move()
            if player.hit(enemy):
                enemies.remove(enemy)
                player.fired_bullets.pop(0)
            if enemy.y + enemy.get_height() >= HEIGHT:
                game.lives -= 1
                enemies.remove(enemy)
        
        draw.drawing(game,player, enemies, FPS)

main()
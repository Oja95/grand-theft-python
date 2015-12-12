import pygame
import textures
import grid
import time
import render
import player
import gameObjects
from random import randint


screen, displayInfo = render.renderInit()

map = grid.getPixelsFromImage("mapvol2.png")

playerModelImage = pygame.image.load("rsz_playermodel.png").convert_alpha()

Exit = False
x = 0
y = 0
spriteList = pygame.sprite.Group()

while not Exit:
    startTime = time.time()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Exit = True
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                Exit = True
            elif i.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
        elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:  # 1 bullet per klikk
            gameObjects.makeBullet(displayInfo)

    key = pygame.key.get_pressed()
    speed = 5
    if key[pygame.K_w]:
        y -= speed
        gameObjects.mobOffset("y", speed)
    elif key[pygame.K_s]:
        y += speed
        gameObjects.mobOffset("y", -speed)
    if key[pygame.K_a]:
        x -= speed
        gameObjects.mobOffset("x", speed)
    elif key[pygame.K_d]:
        x += speed
        gameObjects.mobOffset("x", -speed)

    """ KUI AUTOMAATTULISTAMIST VAJA, HETKEL (RIDA 33) LASEB 1 KUUL PER KLIKK
    if(pygame.mouse.get_pressed() == (1,0,0)):
        gameObjects.makeBullet(displayInfo)
    """

    # MAP RENDER
    mapRectList = render.drawMap(displayInfo, screen, map, x, y)

    # Alumised kaks rida näitab playermodeli rect'i for collision detections. Eemalda 2. rida laters
    #playerModel = pygame.Rect(displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15, 50 ,50 )
    #pygame.draw.rect(screen, textures.blue, playerModel)

    # Player Model(SPRITE) render
    player.drawPlayerModel(displayInfo, playerModelImage, screen)

    # MOBS
    i = randint(1, 100)
    if(i < 5):
        gameObjects.makeMob(displayInfo, 100)  # Generate mob, teine number on HP

    try:
        gameObjects.renderMobs(screen, displayInfo)
    except:
        print("Zombied sõid su ära. kek")
        pygame.quit()  # Ainuke võimalus, kuidas ta siia blokki jõuab on, kui tuleb float division by zero exception
        exit()
        # Ehk siis kui playerimodeli ja mobi vahel distance on 0

    # BULLETS
    gameObjects.renderBullets(screen, displayInfo)
    gameObjects.checkBulletCollision(mapRectList)

    # MOB N BULLET COLLISION
    gameObjects.mobBulletCollision()

    # UPDATE FRAME
    pygame.display.flip()

    # FPS
    endTime = time.time()
    #print(1/(endTime-startTime))

pygame.quit()


# TO DO
# Zombied ei spawniks mapist väljas
# Zombie rotate image vastavalt liikumissuunale
# Levelid, kill counter, mäng mingu järjest raskemaks
# map file
# bullet sprite?
# HP for player?

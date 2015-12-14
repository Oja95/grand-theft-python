import pygame
import grid
import time
import render
import player
import gameObjects
import launcher
import textures
from random import randint


screen, displayInfo = render.renderInit()

map = grid.getPixelsFromImage("images/mapvol2.png")

playerModelImage = pygame.image.load("images/rsz_playermodel.png").convert_alpha()

x = 0  # Initial map scroll position
y = 0

pygame.mouse.set_cursor(*pygame.cursors.broken_x)  # Muudab hiirekursori sihikulaadseks X täheks

launcher.launcher(screen, displayInfo)

Exit = False
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
        #elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:  # 1 bullet per klikk
        #    gameObjects.makeBullet(displayInfo)

    # MAP RENDER
    mapRectList = render.drawMap(displayInfo, screen, map, x, y)

    key = pygame.key.get_pressed()
    speed = 5
    if key[pygame.K_w]:
        # Collision detection playeri ja mapi vahel
        # Kontrollitakse player modelist liikumissuuna poole jäävat piksli värvust. Kui piksel must, siis ei saa liikuda.
        if(screen.get_at((displayInfo.current_w // 2 + 10 , displayInfo.current_h // 2 - 18 )) != (0,0,0,255)):
            y -= speed
            gameObjects.mobOffset("y", speed)
    elif key[pygame.K_s]:
        if(screen.get_at((displayInfo.current_w // 2 + 10 , displayInfo.current_h // 2 + 40)) != (0,0,0,255)):
            y += speed
            gameObjects.mobOffset("y", -speed)
    if key[pygame.K_a]:
        if(screen.get_at((displayInfo.current_w // 2 - 20 , displayInfo.current_h // 2 +5 )) != (0,0,0,255)):
            x -= speed
            gameObjects.mobOffset("x", speed)
    elif key[pygame.K_d]:
        if(screen.get_at((displayInfo.current_w // 2 + 38 , displayInfo.current_h // 2 + 10)) != (0,0,0,255)):
            x += speed
            gameObjects.mobOffset("x", -speed)

    if(pygame.mouse.get_pressed() == (1,0,0)):
        gameObjects.makeBullet(displayInfo)

    # Alumised kaks rida näitab playermodeli rect'i for collision detections. Eemalda 2. rida laters
    #playerModel = pygame.Rect(displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15, 50 ,50 )
    #pygame.draw.rect(screen, textures.blue, playerModel)

    # Player Model(SPRITE) render
    playerModelRect = player.drawPlayerModel(displayInfo, playerModelImage, screen)
    print(playerModelRect)

    # MOBS
    i = randint(1, 1000)
    if(i < gameObjects.killCounter.spawnrate()):  # SPAWNRATE. Tõenäosus, et iga frame spawnib 1 zombie.
        gameObjects.makeMob(displayInfo, 100, screen)  # Generate mob, teine number on HP

    try:
        gameObjects.renderMobs(screen, displayInfo)
    except:
        print("Zombied sõid su ära. kek")
        murderCount = gameObjects.killCounter.output()
        gameObjects.killCounter.setToZero()
        gameObjects.murderAllZombies()
        launcher.launcher(screen, displayInfo, murderCount, restart=True)
        # Ehk siis kui playerimodeli ja mobi vahel distance on 0

    # BULLETS
    gameObjects.renderBullets(screen, displayInfo)
    gameObjects.checkBulletCollision(mapRectList)

    # MOB N BULLET COLLISION
    gameObjects.mobBulletCollision()

    # PRINT SCORE/LEVEL/INFO
    font = pygame.font.Font(None, 36)
    text = font.render("MÕRVADE ARV: " + str(gameObjects.killCounter.output()), 1, (10, 10, 10))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9)
    screen.blit(text, textpos)

    # LEVEL INFO
    text = font.render("SPAWNRATE: " + str(int(gameObjects.killCounter.spawnrate())), 1, (10, 10, 10))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 30)
    screen.blit(text, textpos)

    # ZOMBIE HP
    text = font.render("ZOMBIE HP: " + str(int(gameObjects.killCounter.zombieHP())), 1, (10, 10, 10))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 60)
    screen.blit(text, textpos)

    # UPDATE FRAME
    pygame.display.flip()

    # FPS
    endTime = time.time()
    #print(1/(endTime-startTime))


pygame.quit()


# TO DO
# map file
# HP for player?
# Mob - player collision

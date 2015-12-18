import pygame
import grid
import time
import render
import player
import gameObjects
import launcher
from random import randint, choice

screen, displayInfo = render.renderInit()

map = grid.getPixelsFromImage("images/background.jpg")

# PLAYER MODEL JA ZOMBIE IMAGE PÄRIT OPENGAMEART'ist
# http://opengameart.org/content/animated-top-down-survivor-player
# opengameart.org/content/animated-top-down-zombie
playerModelImage = pygame.image.load("images/rsz_playermodel.png").convert_alpha()

# INIT SOUND
pygame.mixer.init()
gunshots = []
gunshots.append(pygame.mixer.Sound("sounds/gunshot_10.wav"))
gunshots.append(pygame.mixer.Sound("sounds/gunshot_04.wav"))
akSound = pygame.mixer.Sound("sounds/ak.wav")
akSoundLong = pygame.mixer.Sound("sounds/aklong.wav")
# GUNSOUNDS PÄRIT LEHEL FREESPECIALEFFECTS
# http://www.freespecialeffects.co.uk/pages/weapons.html

# SOUNDTRACK: Thomas the dank engine :D
pygame.mixer.music.load("sounds/aylmao.mp3")
pygame.mixer.music.play()

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
        elif(not gameObjects.playerHP.hasRifle):
            if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:  # 1 bullet per klikk
                gameObjects.makeBullet(displayInfo)
                soundfx = choice(gunshots)
                soundfx.play()

    # MAP RENDER
    mapRectList = render.drawMap(displayInfo, screen, map, x, y)

    key = pygame.key.get_pressed()

    # PLAYER - MAP COLLISION DETECTION + MOVEMENT
    speed = 5 # MOVEMENT SPEED
    if key[pygame.K_w]:
        # Kontrollitakse player modelist liikumissuuna poole jäävat piksli värvust. Kui piksel must, siis ei saa liikuda.
        if(screen.get_at((displayInfo.current_w // 2 + 10 , displayInfo.current_h // 2 - 18 )) != (0,0,0,255)):
            y -= speed
            gameObjects.Offset("y", speed)
    elif key[pygame.K_s]:
        if(screen.get_at((displayInfo.current_w // 2 + 10 , displayInfo.current_h // 2 + 40)) != (0,0,0,255)):
            y += speed
            gameObjects.Offset("y", -speed)
    if key[pygame.K_a]:
        if(screen.get_at((displayInfo.current_w // 2 - 20 , displayInfo.current_h // 2 +5 )) != (0,0,0,255)):
            x -= speed
            gameObjects.Offset("x", speed)
    elif key[pygame.K_d]:
        if(screen.get_at((displayInfo.current_w // 2 + 38 , displayInfo.current_h // 2 + 10)) != (0,0,0,255)):
            x += speed
            gameObjects.Offset("x", -speed)

    if(gameObjects.playerHP.hasRifle):
        # AUTOMAATTULISTAMINE
        if(pygame.mouse.get_pressed() == (1,0,0)):
            gameObjects.makeBullet(displayInfo)
            if(gameObjects.playerHP.ammo == 1):
                pygame.mixer.stop()
                akSoundLong.play()
            else:
                akSound.play()
            gameObjects.playerHP.decrementAmmo()
            if(gameObjects.playerHP.ammo < 1):
                gameObjects.playerHP.loseRifle()

    # PLAYER MODEL (SPRITE) RENDER
    playerModelRect = player.drawPlayerModel(displayInfo, playerModelImage, screen)

    # SPAWN MOBS
    i = randint(1, 1000)
    if(i < gameObjects.killCounter.spawnrate()):  # SPAWNRATE. Tõenäosus, et iga frame spawnib 1 zombie.
        gameObjects.makeMob(displayInfo, gameObjects.killCounter.zombieHP(), screen)  # Generate mob, teine number on HP

    # SPAWN HP PACKS
    i = randint(1, 300)
    if(i == 1):
        gameObjects.createHpPack(screen, displayInfo)

    # RENDER HP PACKS
    gameObjects.renderHealthPacks(screen)

    # SPAWN RIFLE PICKUP
    i = randint(1,500)
    if(i == 1):
        gameObjects.createRifle(screen, displayInfo)

    # RENDER RIFLE PICKUP
    gameObjects.renderRiflePickup(screen)

    # CHECK RIFLE PICKUP COLLISION WITH PLAYAH
    gameObjects.playerRifleCollision(playerModelRect)

    # UPDATE MOB ASUKOHT
    gameObjects.renderMobs(screen, displayInfo)

    # KUI PLAYER HP ALLA NULLI, MÄNG LÕPETAB JA VISKAB ETTE ALGSE MENÜÜ
    if(gameObjects.playerHP.hp <= 0):
        #print("Zombied sõid su ära. kek")
        murderCount = gameObjects.killCounter.output()
        gameObjects.killCounter.setToZero()
        gameObjects.playerHP.setHP(100)
        gameObjects.murderAllZombies()
        launcher.launcher(screen, displayInfo, murderCount, restart=True)


    # DRAW BULLETS + CHECK COLLISION
    gameObjects.renderBullets(screen, displayInfo)
    gameObjects.checkBulletCollision(mapRectList)

    # MOB N BULLET COLLISION
    gameObjects.mobBulletCollision()

    # PLAYER N MOB COLLISION
    gameObjects.playerMobCollision(playerModelRect)

    # PLAYER N HP PACK COLLISION
    gameObjects.playerHpCollision(playerModelRect)

    ### USER INTERFACE IN-GAME
    # KILL COUNT
    font = pygame.font.Font(None, 36)
    text = font.render("MÕRVADE ARV: " + str(gameObjects.killCounter.output()), 1, (255, 255, 255))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9)
    screen.blit(text, textpos)

    # PLAYER HP
    if(gameObjects.playerHP.output() < 51):  # Kui HP alla 50, kuva punaselt
        text = font.render("HEALTH: " + str(gameObjects.playerHP.output()), 1, (255, 10, 10))
    else:
        text = font.render("HEALTH: " + str(gameObjects.playerHP.output()), 1, (255, 255, 255))

    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 30)
    screen.blit(text, textpos)

    # AK-47 INFO, KAS ON AK JA PALJU KUULE
    text = font.render("AK-47 OLEMAS?: " + str(gameObjects.playerHP.hasRifle), 1, (255, 255, 255))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 60)
    screen.blit(text, textpos)

    if(gameObjects.playerHP.hasRifle == True):
        text = font.render("AK-47 KUULE: " + str(int(gameObjects.playerHP.ammo)), 1, (255, 255, 255))
        textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 90)
        screen.blit(text, textpos)

    # LEVEL INFO
    text = font.render("SPAWNRATE: " + str(int(gameObjects.killCounter.spawnrate())), 1, (255, 255, 255))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 120)
    screen.blit(text, textpos)

    # ZOMBIE HP
    text = font.render("ZOMBIE HP: " + str(int(gameObjects.killCounter.zombieHP())), 1, (255, 255, 255))
    textpos = text.get_rect(centerx=displayInfo.current_w*5/6, centery=displayInfo.current_h*1/9 + 150)
    screen.blit(text, textpos)
    ### END OF USER INTERFACE IN-GAME

    # UPDATE FRAME
    pygame.display.flip()

    # FPS
    endTime = time.time()
    #print(1/(endTime-startTime))


pygame.quit()

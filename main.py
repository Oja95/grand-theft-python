import pygame
import textures
import grid
import time
import render
import player
import gameObjects


screen,displayInfo = render.renderInit()
# Monitor info:

#checkers = grid.genCheckers()
map = grid.getPixelsFromImage("newmap.tiff")

playerModelImage = pygame.image.load("playermodel.tif")

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

    key = pygame.key.get_pressed()
    speed = 5
    if key[pygame.K_w]:
        y -= speed
    elif key[pygame.K_s]:
        y += speed
    if key[pygame.K_a]:
        x -= speed
    elif key[pygame.K_d]:
        x += speed


    render.drawMap(displayInfo,screen,map,x,y)

    # Alumised kaks rida näitab playermodeli rect'i for collision detections
    playerModel = pygame.Rect(displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15, 30 ,30 )
    pygame.draw.rect(screen, textures.blue, playerModel)
    # Player Model render
    player.drawPlayerModel(displayInfo, playerModelImage, screen)


    if(pygame.mouse.get_pressed() == (1,0,0)):
        gameObjects.makeBullet(displayInfo)


    gameObjects.renderBullets(screen, displayInfo)
    pygame.display.flip()
    endTime = time.time()
    #print(1/(endTime-startTime))

pygame.quit()

import pygame
import sys
import textures
import random
import grid
import time
import player

pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
pygame.display.set_caption("Grand Theft Python")  # Akna nimesilt.
screen.fill(textures.purple)
pygame.display.flip()

# Monitor info:
print(displayInfo.current_w, displayInfo.current_h)
# Loeme pildifailist pikslid

#checkers = grid.genCheckers()
checkers = grid.getPixelsFromImage("map.tiff")

playerModelImage = pygame.image.load("playermodel.tif")

Exit = False
x = 0
y = 0
while not Exit:
    startTime = time.time()

    # KEYBOARD INTERACTIONS
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

    if(pygame.mouse.get_pressed()[0]):
        #playerModel.shoot()
        pass

    #Current render engine
    for i in range((displayInfo.current_w) // grid.tileSize + 4):
        for j in range((displayInfo.current_h)//grid.tileSize + 4):
            #Tile coordinates
            X = ((i-2) * grid.tileSize) - x % grid.tileSize
            Y = ((j-2) * grid.tileSize) - y % grid.tileSize
            tile = grid.genTile(X,Y,grid.tileSize)
            if checkers[i + x//grid.tileSize][j + y//grid.tileSize] == [0, 0, 0]:
                grid.drawGridTile(screen,textures.black,tile)
            elif checkers[i + x//grid.tileSize][j + y//grid.tileSize] == [255, 255, 255]:
                grid.drawGridTile(screen,textures.white,tile)
            else:
                grid.drawGridTile(screen,textures.green,tile)
    # Player model ekraani keskele.

    player.drawPlayerModel(displayInfo, playerModelImage, screen)

    pygame.display.flip()

    endTime = time.time()
    #print(1/(endTime-startTime))
# Spaghetti and meatballs test

pygame.quit()

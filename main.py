import pygame
import sys
import textures
import random
import grid
import time
import render


screen,displayInfo = render.renderInit()
# Monitor info:
print(displayInfo.current_w,displayInfo.current_h)
# Loeme pildifailist pikslid

#checkers = grid.genCheckers()
map = grid.getPixelsFromImage("dickbutt.tif")

Exit = False
x = 0
y = 0
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
    speed = 30
    if key[pygame.K_w]:
        y -= speed
    elif key[pygame.K_s]:
        y += speed
    if key[pygame.K_a]:
        x -= speed
    elif key[pygame.K_d]:
        x += speed

    render.drawMap(displayInfo,screen,map,x,y)
    pygame.draw.rect(screen, textures.blue, render.playerRect(displayInfo))
    pygame.display.flip()
    endTime = time.time()
    print(1/(endTime-startTime))


pygame.quit()

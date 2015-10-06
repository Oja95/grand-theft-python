import pygame
import sys
import textures
import random
import grid
import time

# map = grid.getGrid("grid.txt")

pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
pygame.display.set_caption("Grand Theft Python")  # Akna nimesilt.
screen.fill(textures.purple)
pygame.display.flip()

# Monitor info:
print(displayInfo.current_w, displayInfo.current_h)

checkers = grid.genCheckers()

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
    if key[pygame.K_w]:
        y += 5
    elif key[pygame.K_s]:
        y -= 5
    if key[pygame.K_a]:
        x += 5
    elif key[pygame.K_d]:
        x -= 5


    for i in range((displayInfo.current_w) // grid.tileSize + 4):
        for j in range((displayInfo.current_h)//grid.tileSize + 4):
            X = (i-2) * grid.tileSize + x % grid.tileSize
            Y = (j-2) * grid.tileSize + y % grid.tileSize
            if checkers[i + x // grid.tileSize][j + y // grid.tileSize] == 0:
                grid.drawGridTile(X, Y, screen, grid.tileSize, textures.black)
            else:
                grid.drawGridTile(X, Y, screen, grid.tileSize, textures.white)

    # Player model ekraani keskele.
    playerModel = pygame.Rect(displayInfo.current_w // 2, displayInfo.current_h // 2, 50, 50)
    pygame.draw.rect(screen, textures.green, playerModel)

    pygame.display.flip()

    endTime = time.time()
    print(1/(endTime-startTime))
"""
screen.scroll(x,y)
pygame.display.flip()
x,y=0,0
"""

pygame.quit()

import pygame
import sys
import textures
import random
import grid
map = grid.getGrid("grid.txt")


pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
pygame.display.set_caption("Grand Theft Python")  # Akna nimesilt.
screen.fill(textures.purple)
pygame.display.flip()

#startpos
pxpos = 500*grid.tileSize//2
pypos = 500*grid.tileSize//2



#katsetused gridi joonistamiseks, AJUTINE

checkers = grid.genCheckers()


Exit = False
x = 0
y = 0
while not Exit:
    #Esc viskab pygamest välja
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
        y-=1
    elif key[pygame.K_s]:
        y+=1
    if key[pygame.K_a]:
        x-=1
    elif key[pygame.K_d]:
        x+=1
    for i in range((displayInfo.current_w)//grid.tileSize):
        for j in range((displayInfo.current_h)//grid.tileSize):
            if checkers[i+x//grid.tileSize][j+y//grid.tileSize] == 0:
                grid.drawGridTile(i*grid.tileSize+x%grid.tileSize,j*grid.tileSize+y%grid.tileSize,screen,grid.tileSize,textures.black)
            else:
                grid.drawGridTile(i*grid.tileSize+x%grid.tileSize,j*grid.tileSize+y%grid.tileSize,screen,grid.tileSize,textures.white)
    pygame.display.flip()
"""
screen.scroll(x,y)
pygame.display.flip()
x,y=0,0
"""

pygame.quit()

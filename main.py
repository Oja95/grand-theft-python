import pygame
import sys
import textures
import random
import grid
map = grid.getGrid("grid.txt")
print(map)

pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
screen = pygame.display.set_mode((600,800))
screen.fill(textures.purple)
pygame.display.flip()


#katsetused gridi joonistamiseks, AJUTINE
for i in range((displayInfo.current_w)//grid.tileSize):
    for j in range((displayInfo.current_h)//grid.tileSize):
        grid.drawGridTile(i,j,screen,grid.tileSize,[random.randint(0,255),random.randint(0,255),random.randint(0,255)],True)
pygame.display.flip()


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
    elif key[pygame.K_a]:
        x-=1
    elif key[pygame.K_s]:
        y+=1
    elif key[pygame.K_d]:
        x+=1
    screen.scroll(x,y)
    pygame.display.flip()
    x,y=0,0
pygame.quit()

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
screen.fill(textures.purple)
pygame.display.flip()


#katsetused gridi joonistamiseks, AJUTINE
for i in range((displayInfo.current_w)//grid.tileSize):
    for j in range((displayInfo.current_h)//grid.tileSize):
        grid.drawGridTile(i,j,screen,grid.tileSize,[random.randint(0,255),random.randint(0,255),random.randint(0,255)],True)
     
pygame.display.flip()

Exit = False
while not Exit:
    #Esc viskab pygaest välja
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Exit = True
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                Exit = True
            elif i.key == pygame.K_a:
                pygame.display.toggle_fullscreen()
pygame.quit()

import pygame
import sys
import textures
import random
from grid import getGrid, drawGridTile # Funktsioon, mis loeb failis gridi sisse

map = getGrid("grid.txt")
print(map)

pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
screen.fill(textures.purple)
pygame.display.flip()

for i in range((displayInfo.current_w)//15):
    for j in range((displayInfo.current_h)//15):
        drawGridTile(i,j,screen,15,[random.randint(0,255),random.randint(0,255),random.randint(0,255)],True)
     
pygame.display.flip()

"""while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
    key = pygame.key.get_pressed()
    if(key[pygame.K_a]) : pygame.display.toggle_fullscreen()
    if(key[pygame.K_q]) : sys.exit()
    # Testimiseks, a paneb fullscreen, q - quit

"""
Exit = False
while not Exit:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Exit = True
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                Exit = True
pygame.quit()

import pygame
import sys

pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    key = pygame.key.get_pressed()
    if(key[pygame.K_a]) : pygame.display.toggle_fullscreen()
    if(key[pygame.K_q]) : sys.exit()

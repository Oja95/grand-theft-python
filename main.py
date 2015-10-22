import pygame
import textures
import grid
import time
import render
import player


screen,displayInfo = render.renderInit()
# Monitor info:
print(displayInfo.current_w,displayInfo.current_h)
# Loeme pildifailist pikslid

#checkers = grid.genCheckers()
map = grid.getPixelsFromImage("newmap.tiff")

playerModelImage = pygame.image.load("playermodel.tif")

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

    #player.drawPlayerModel(displayInfo, playerModelImage, screen)

    playerModel = pygame.Rect(displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15, 30 ,30 )
    pygame.draw.rect(screen, textures.blue, playerModel)
    rotatedImage = player.getPlayerModelDirection(playerModelImage, displayInfo)
    screen.blit(rotatedImage, ((displayInfo.current_w // 2 - 15), (displayInfo.current_h // 2 -15)) )

    pygame.display.flip()
    endTime = time.time()
    print(1/(endTime-startTime))


pygame.quit()

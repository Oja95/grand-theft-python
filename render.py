import pygame
import textures
import grid



def renderInit():
    pygame.init()
    displayInfo = pygame.display.Info()
    screen = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
    pygame.display.set_caption("Grand Theft Python")  # Akna nimesilt.
    screen.fill(textures.purple)
    pygame.display.flip()
    return screen,displayInfo


def playerRect(displayInfo):
    # Player model ekraani keskele.
    return pygame.Rect(displayInfo.current_w // 2, displayInfo.current_h // 2, 30 ,30 )

#py,px = player pos
def drawMap(displayInfo,screen,map,px,py):
    #Current render engine
    for i in range((displayInfo.current_w) // grid.tileSize + 4):
        for j in range((displayInfo.current_h)//grid.tileSize + 4):
            #Tile coordinates
            X= ((i-2) * grid.tileSize) - px % grid.tileSize
            Y = ((j-2) * grid.tileSize) - py % grid.tileSize
            tile = grid.genTile(X,Y,grid.tileSize)
            try:
                mapx = i + px//grid.tileSize
                mapy = j + py//grid.tileSize
                if mapx >= 0 and mapy >= 0:
                    grid.drawGridTile(screen,map[mapy][mapx],tile)
                else:
                    grid.drawGridTile(screen,textures.purple,tile)
            except:
                grid.drawGridTile(screen,textures.purple,tile)

#Var tileSize hold the current tile size, used in rendering
tileSize = 30
import pygame
import textures
def getGrid(filename):
    f = open(filename)
    grid = f.read()
    grid = grid.replace(" ", "")
    grid = grid.split("\n")
    newGrid = []
    for line in grid:
        newGrid.append(list(line))
    return newGrid

#Draws one grid tile at coordinates, on var=screen with color
def drawGridTile(x,y,screen,tileSize,color,display=False):
    tile = pygame.Rect(x*tileSize,y*tileSize,tileSize,tileSize)
    pygame.draw.rect(screen,color,tile)
    


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
def drawGridTile(x,y,screen,tileSize,color):
    tile = pygame.Rect(x,y,tileSize,tileSize)
    pygame.draw.rect(screen,color,tile)
    
def genCheckers():
    newCheckers = []
    for i in range(500):
        newCheckers.append([])
        for j in range(500):
            if i%2==0 and j%2==0:
                newCheckers[i].append(1)
            else:
                newCheckers[i].append(0)
    return newCheckers






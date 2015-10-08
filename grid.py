from PIL import Image
import pygame
import textures

#Var tileSize hold the current tile size, used in rendering
tileSize = 30

#Draws one grid tile at coordinates, on var=screen with color
def drawGridTile(x,y,screen,tileSize,color):
    tile = pygame.Rect(x,y,tileSize,tileSize)
    pygame.draw.rect(screen,color,tile)
    
def genCheckers():
    newCheckers = []
    for i in range(500):
        newCheckers.append([])
        for j in range(500):
            if i%2==0 or j%2==0:
                newCheckers[i].append(1)
            else:
                newCheckers[i].append(0)
    return newCheckers

def getPixelsFromImage(file):
    im = Image.open(file, 'r')
    width, height = im.size
    pixel_values = list(im.getdata())
    pixelList = []
    aPixel = []
    for i in range(width*height):
        for j in range(3):
            aPixel.append(pixel_values[i][j])
        pixelList.append(aPixel)
        aPixel = []
    # Pikslid vaja saada 2d arraysse width * height

    pixel2dList = []
    counter = 0
    for i in range(height):
        pixel2dList.append([])
        for j in range(width):
            pixel2dList[i].append(pixelList[counter])
            counter += 1
    return pixel2dList

# pixel2dlist kujul list[kõrgus][laius]

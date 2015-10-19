import pygame
import math

def getVectorLenght(vector):
    return math.sqrt((vector[0] ** 2) + (vector[1] ** 2))


def setPlayerModelDirection(image, displayInfo):
    mousePos = pygame.mouse.get_pos()
    playerModelAsukoht = [(displayInfo.current_w // 2 -15), (displayInfo.current_h // 2 - 15)]
    yAxis = [displayInfo.current_w // 2 -15, displayInfo.current_h-1]

    # Teha 2 tsooni. Vasak/parem. vasakul tsoonis positiivne, paremas negatiivne.

    mouseVector = [mousePos[0] - playerModelAsukoht[0], mousePos[1] - playerModelAsukoht[1]]
    yAxisVector = [yAxis[0] - playerModelAsukoht[0], yAxis[1] - playerModelAsukoht[1]]
    yAxisVectorLenght = math.sqrt((yAxisVector[0] ** 2) + (yAxisVector[1] ** 2))
    mouseVectorLenght = math.sqrt((mouseVector[0] ** 2)+ (mouseVector[1] ** 2))
    cosAngle = (mouseVector[0]*yAxisVector[0] + mouseVector[1]*yAxisVector[1]) / (yAxisVectorLenght*mouseVectorLenght)
    angle = math.acos(cosAngle)
    angle = 180 - math.degrees(angle)

    if(mousePos[0] > displayInfo.current_w // 2 - 15): angle = -angle
    return pygame.transform.rotate(image, angle)


# Playermodel keskkoht koordinaadid: 785 435
#pygame.init()
#dispinf = pygame.display.Info()
#setPlayerModelDirection(0, dispinf)

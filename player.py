import pygame
import math

def getVectorLenght(vector):
    return math.sqrt((vector[0] ** 2) + (vector[1] ** 2))

def rot_center(image, angle): # Rotateb imaget keskpunkti järgi
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def getPlayerModelDirection(image, displayInfo):
    # Muudab player modeli suunda vastavalt hiire asukohale.
    mousePos = pygame.mouse.get_pos()
    playerModelAsukoht = [(displayInfo.current_w // 2 -15), (displayInfo.current_h // 2 - 15)]
    yAxis = [displayInfo.current_w // 2 -15, displayInfo.current_h-15]

    # Teha 2 tsooni. Vasak/parem. vasakul tsoonis positiivne, paremas negatiivne.

    mouseVector = [mousePos[0] - playerModelAsukoht[0], mousePos[1] - playerModelAsukoht[1]]
    yAxisVector = [yAxis[0] - playerModelAsukoht[0], yAxis[1] - playerModelAsukoht[1]]
    yAxisVectorLenght = math.sqrt((yAxisVector[0] ** 2) + (yAxisVector[1] ** 2))
    mouseVectorLenght = math.sqrt((mouseVector[0] ** 2)+ (mouseVector[1] ** 2))
    cosAngle = (mouseVector[0]*yAxisVector[0] + mouseVector[1]*yAxisVector[1]) / (yAxisVectorLenght*mouseVectorLenght)
    angle = math.acos(cosAngle)
    angle = 180 - math.degrees(angle)

    if(mousePos[0] > displayInfo.current_w // 2 - 15): angle = -angle  # koosinus I ja IV veerand positiivne, II ja III negatiivne
    angle += 90  # Pilt on 90 kraadi nihkes.
    return rot_center(image, angle)


def drawPlayerModel(displayInfo, playerModelImage, screen):
    playerModel = pygame.Rect(displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15, 50 ,50 )
    rotatedImage = getPlayerModelDirection(playerModelImage, displayInfo)
    screen.blit(rotatedImage, ((displayInfo.current_w // 2 - 15), (displayInfo.current_h // 2 -15)) )

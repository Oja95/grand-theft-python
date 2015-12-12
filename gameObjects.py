import textures
import pygame
import math
from random import randint


class Mob(pygame.sprite.Sprite):
    def __init__(self, displayInfo, player, health):
        pygame.sprite.Sprite.__init__(self)

        self.player = player  # Playermodeli asukoht, et mob teaks kuhu suunas liikuda.

        #self.image = pygame.Surface([30,30])
        self.image = pygame.image.load("mob.png").convert_alpha()
        #self.image.fill(textures.blue)

        self.health = health  # vastavalt levelile võib panna zombied tugevamaks.

        self.rect = self.image.get_rect()
        # Spawnime Mobi nii, et mob oleks 30 px äärest.
        side = randint(0,3) # Mis küljele spawnib. 0-vasak, 1-parem,2-lagi,3-põhi
        if(side == 0):
            self.rect[0] = 0
            self.rect[1] = randint(30, displayInfo.current_h-30)
        if(side == 1):
            self.rect[0] = displayInfo.current_w - 30
            self.rect[1] = randint(30, displayInfo.current_h-30)
        if(side == 2):
            self.rect[0] = randint(30, displayInfo.current_w-30)
            self.rect[1] = 0
        if(side == 3):
            self.rect[0] = randint(30, displayInfo.current_w-30)
            self.rect[1] = displayInfo.current_h - 30

    def moveTowardsPlayer(self):
        speed = 1
        distance = [self.rect[0] - self.player[0], self.rect[1] - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        """ Kui tuleb exception float divide by 0
        if(norm == 0):
            direction = [distance[0] / 0.0001 , distance[1] / 0.0001]
        else:
            direction = [distance[0] / norm, distance[1] / norm]
        """
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= bullet_vector[0]
        self.rect.y -= bullet_vector[1]


class Bullet(pygame.sprite.Sprite):

    def __init__(self, mouse, player):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 4])
        self.image.fill(textures.red)

        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.player = player

        self.damage = 50

        self.rect = self.image.get_rect()
        self.rect[0] = self.player[0] + 15
        self.rect[1] = self.player[1] + 15

    def update(self):

        speed = -15
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        """ Kui tuleb exception float divide by 0
        if(norm == 0):
            direction = [distance[0] / 0.0001 , distance[1] / 0.0001]
        else:
            direction = [distance[0] / norm, distance[1] / norm]
        """
        if(norm == 0): norm = 0.01
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= bullet_vector[0]
        self.rect.y -= bullet_vector[1]

    def mobCollision(self):
        pass

spriteList = pygame.sprite.Group()
mobList = pygame.sprite.Group()

# BULLET

def checkBulletCollision(mapRectList):
    for bullet in spriteList:
        for rect, color in mapRectList:
            if(rect.contains(bullet.rect) and color == [0, 18, 255]):
                spriteList.remove(bullet)


def makeBullet(displayInfo):
    bullet = Bullet(pygame.mouse.get_pos(), [displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15])
    spriteList.add(bullet)

def renderBullets(screen, displayInfo):
    for sprite in spriteList:
        if(sprite.rect[0] > displayInfo.current_w  or sprite.rect[1] > displayInfo.current_h or sprite.rect[0] < 0 or sprite.rect[1] < 0):
            spriteList.remove(sprite)
        sprite.update()
    spriteList.draw(screen)

# MOB
# FOR FUCKS SAKES, spaghetti code
def makeMob(displayInfo, health):
    mob = Mob(displayInfo, [displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15], health)
    mobList.add(mob)

def renderMobs(screen, displayInfo):
    for mob in mobList:
        mob.moveTowardsPlayer()
    mobList.draw(screen)

def mobOffset(direction, speed):
    for mob in mobList:
        if(direction == "y"):
            mob.rect[1] += speed
        else:
            mob.rect[0] += speed

# MOB N BULLET COLLISION
def mobBulletCollision():
    for bullet in spriteList:
        for mob in mobList:
            if(mob.rect.contains(bullet.rect)):
                spriteList.remove(bullet)
                mob.health -= bullet.damage
                if(mob.health < 1):
                    mobList.remove(mob)
                if(mob.health <= 50):
                    # Kui pihta saab, kuva teine sprite?
                    #mob.image.fill(textures.red)
                    pass




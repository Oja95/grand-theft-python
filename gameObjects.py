import pygame
import textures
import math
from random import randint

class Mob(pygame.sprite.Sprite):
    def __init__(self, displayInfo, player, health):
        pygame.sprite.Sprite.__init__(self)

        self.player = player  # Playermodeli asukoht, et mob teaks kuhu suunas liikuda.
        self.nurk = 90  # Init suund(kraadides)

        self.image = pygame.image.load("images/mob.png").convert_alpha()
        self.copy = self.image

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
        speed = 2  # Kiirus min 2, sest 2 tundi debugimist ütleb nii
        distance = [self.rect[0] - self.player[0], self.rect[1] - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        mob_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= mob_vector[0]
        self.rect.y -= mob_vector[1]
        self.image = pygame.transform.rotate(self.copy, self.getNurk())

    # MOB SUUNA MUUTMINE VASTAVALT PLAYER MODEL ASUKOHALE
    # Siin tuleb nüüd kõrgem matemaatika. Võrreldes playermodeli suuna muutmisele(oli sama pilt koguaeg, mille suunda
    # muutsime koguaeg teatud nurga võrra), siis siin on nii, et suunda muutes, meil pildi nurk muutub koguaeg
    # Ehk hoiame mälus eelmist nurka(init = 90), ja siis leiame iga frame jaoks nurga palju pöörama peame
    # seejärel liidame/lahutame ja ongi magic

    def getNurk(self):
        diagonaal = math.sqrt(abs(self.rect.x - self.player[0]) ** 2 + abs(self.rect.y - self.player[1]) ** 2)
        yPikkus = self.rect.x - self.player[0]
        nurk = math.degrees(math.acos(yPikkus/diagonaal))
        if(self.rect.y > self.player[1]):
            return -nurk+180
        else:  # NO IDEA KUIDAS VÕI MIKS SEE TÖÖTAB.
            return nurk+180

class Bullet(pygame.sprite.Sprite):

    def __init__(self, mouse, player):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 4])
        self.image.fill(textures.white)

        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.player = player

        self.damage = 50

        self.rect = self.image.get_rect()
        self.rect[0] = self.player[0] + 15
        self.rect[1] = self.player[1] + 15

    def update(self):

        speed = -38
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        if(norm == 0): norm = 0.01
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= bullet_vector[0]
        self.rect.y -= bullet_vector[1]

    def mobCollision(self):
        pass

class killCounter():
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def output(self):
        return self.count


spriteList = pygame.sprite.Group()
mobList = pygame.sprite.Group()

# BULLET

def checkBulletCollision(mapRectList):  # Bullet collision mapiga
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
def makeMob(displayInfo, health):
    mob = Mob(displayInfo, [displayInfo.current_w // 2 - 25, displayInfo.current_h // 2 - 25], health)
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
killCounter = killCounter()  # Palju zombiesid mõrvatud on

def mobBulletCollision():
    for bullet in spriteList:
        for mob in mobList:
            if(mob.rect.contains(bullet.rect)):
                spriteList.remove(bullet)
                mob.health -= bullet.damage
                if(mob.health < 1):
                    mobList.remove(mob)
                    killCounter.increment()
                if(mob.health <= 50):
                    # Kui pihta saab, kuva teine sprite?
                    #mob.image.fill(textures.red)
                    pass


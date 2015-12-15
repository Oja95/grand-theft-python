import pygame
import textures
import math
from random import randint

class healthPack(pygame.sprite.Sprite):

    # Health pack pickup playerile. Annab HP'd, kui collideb

    def __init__(self, screen, displayInfo):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/healthpack.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.hp = 25  # Kui palju HP annab

        screen.set_at((0,0), (0,0,0,255))
        while(screen.get_at((self.rect[0], self.rect[1])) == (0,0,0,255)):
            # Määrame asukoha. Random spawn
            self.rect[0] = randint(30, displayInfo.current_w - 30)
            self.rect[1] = randint(30, displayInfo.current_h - 30)

class Rifle(pygame.sprite.Sprite):

    # Automaatrelv pick-up

    def __init__(self, screen, displayInfo):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/rifle.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.bullets = 90  # Mitu kuuli automaatrelvaga lasta saad

        screen.set_at((0,0), (0,0,0,255))
        while(screen.get_at((self.rect[0], self.rect[1])) == (0,0,0,255)):
            # Määrame asukoha. Random spawn
            self.rect[0] = randint(30, displayInfo.current_w - 30)
            self.rect[1] = randint(30, displayInfo.current_h - 30)


class Mob(pygame.sprite.Sprite):

    # Tekitab mob'i, liigub playeri suunas

    def __init__(self, displayInfo, player, health, screen):

        pygame.sprite.Sprite.__init__(self)

        self.player = player  # Playermodeli asukoht, et mob teaks kuhu suunas liikuda.
        self.nurk = 90  # Mob sprite on 90 kraadi nihkes.

        self.image = pygame.image.load("images/mob.png").convert_alpha()
        self.copy = self.image  # Teeme pildist koopia, et ei peaks originaalset pilti pöörama

        self.health = health  # Vastavalt killcount'ile zombie HP suureneb

        self.rect = self.image.get_rect()  # Zombie asukoht display'l

        screen.set_at((0,0), (0,0,0,255))  # Nasty hack - Tiit seletab
        while(screen.get_at((self.rect[0], self.rect[1])) == (0,0,0,255)):  # Ei lase mobil spawnida mapist välja
            side = randint(0,3)
            if(side == 0): # vasak
                self.rect[0] = 0
                self.rect[1] = randint(30, displayInfo.current_h-30)
            if(side == 1): # top
                self.rect[0] = randint(30, displayInfo.current_w-30)
                self.rect[1] = 0
            if(side == 2): # parem
                self.rect[0] = displayInfo.current_w - 30
                self.rect[1] = randint(30, displayInfo.current_h-30)
            if(side == 3): # põhi
                self.rect[0] = randint(30, displayInfo.current_w-30)
                self.rect[1] = displayInfo.current_h - 30

    def moveTowardsPlayer(self):
        speed = 2  # Kiirus min 2, sest 2 tundi debugimist ütleb nii
        distance = [self.rect[0] - self.player[0], self.rect[1] - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        if(norm == 0): norm = 0.1  # Väldime divison by zero exceptionit, nasty hack
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
        if(diagonaal == 0): diagonaal = 0.1  # Väldime division by zero exceptionit. nasty hack
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

        speed = -50
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        if(norm == 0): norm = 0.01
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= bullet_vector[0]
        self.rect.y -= bullet_vector[1]


class killCounter():
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def output(self):
        return self.count

    def setToZero(self):
        self.count = 0

    def spawnrate(self):
        # Funktsioon muudab vastavalt kill countile lineaarselt spawnrate.
        # Kills = 0  ->  Spawnrate tõenäosus = 25/1000
        # Kills = 1500 -> Spawnrate tõenäosus = 950/1000
        return 37*self.count/60 + 25

    def zombieHP(self):
        # Funktsioon muudab vastavalt kill countile lineaarselt zombie HP.
        # Kills = 0 -> HP = 100
        # Kills = 1500 -> HP = 400
        return self.count/5 + 100


class playerHP():
    def __init__(self):
        self.hp = 100
        self.hasRifle = False
        self.ammo = 0

    def getHit(self, damage):
        self.hp -= damage

    def setHP(self, hp):
        self.hp = hp

    def output(self):
        return self.hp

    def getHeal(self, hp):
        self.hp += hp

    def giveRifle(self):
        self.hasRifle = True

    def giveAmmo(self, ammo):
        self.ammo += ammo

    def decrementAmmo(self):
        self.ammo -= 1

    def loseRifle(self):
        self.hasRifle = False


# Spaghetti code below this line

# Konteinerid, mis hoiavad mängu objekte
spriteList = pygame.sprite.Group()  # Bulletid
mobList = pygame.sprite.Group()  # Zombied
hpList = pygame.sprite.Group()  # HP Pack sprite group
rifleList = pygame.sprite.Group()  # Rifle pickup group

# BULLET FUNKTSIOONID

def checkBulletCollision(mapRectList):  # Bullet collision mapiga
    for bullet in spriteList:
        for rect, color in mapRectList:
            if(rect.contains(bullet.rect) and color == [0, 0, 0]):  # [0,0,0] ehk siis must pixel RGB, on mapist väljas
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

# MOB FUNKTSIOONID

def makeMob(displayInfo, health, screen):
    mob = Mob(displayInfo, [displayInfo.current_w // 2 - 10, displayInfo.current_h // 2 - 10], health,  screen)
    mobList.add(mob)

def renderMobs(screen, displayInfo):
    for mob in mobList:
        mob.moveTowardsPlayer()
    mobList.draw(screen)

def Offset(direction, speed):
    for mob in mobList:
        if(direction == "y"):
            mob.rect[1] += speed
        else:
            mob.rect[0] += speed

    for hpPack in hpList:
        if(direction == "y"):
            hpPack.rect[1] += speed
        else:
            hpPack.rect[0] += speed

    for rifle in rifleList:
        if(direction == "y"):
            rifle.rect[1] += speed
        else:
            rifle.rect[0] += speed

# MOB N BULLET COLLISION
killCounter = killCounter()

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

# FUNKTSIOON KAOTAB KÕIK ZOMBIE'D ÄRA
def murderAllZombies():
    for mob in mobList:
        mobList.remove(mob)


# MOB - PLAYER COLLISION + DAMAGE TO PLAYER
playerHP = playerHP()
def playerMobCollision(playerModelRect):
    for mob in mobList:
        if(mob.rect.colliderect(playerModelRect)):
            playerHP.getHit(1)


# HEALTHPACK SPAWN
def createHpPack(screen, displayInfo):
    hpPack = healthPack(screen, displayInfo)
    hpList.add(hpPack)

# RENDER HP PACK
def renderHealthPacks(screen):
    for hppack in hpList:
        hppack.update()
    hpList.draw(screen)

# HP PACK - PLAYER COLLISION
def playerHpCollision(playerModelRect):
    for hppack in hpList:
        if(hppack.rect.colliderect(playerModelRect)):
            playerHP.getHeal(hppack.hp)
            hpList.remove(hppack)

# RIFLE PICKUP SPAWN
def createRifle(screen, displayInfo):
    rifle = Rifle(screen, displayInfo)
    rifleList.add(rifle)

def renderRiflePickup(screen):
    for rifle in rifleList:
        rifle.update()
    rifleList.draw(screen)

def playerRifleCollision(playerModelRect):
    for rifle in rifleList:
        if(rifle.rect.colliderect(playerModelRect)):
            playerHP.giveRifle()
            playerHP.giveAmmo(rifle.bullets)
            rifleList.remove(rifle)



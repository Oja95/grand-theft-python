import textures
import pygame
import math

class Bullet(pygame.sprite.Sprite):

    def __init__(self, mouse, player):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 4])
        self.image.fill((255,0,0))

        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.player = player

        self.rect = self.image.get_rect()
        self.rect[0] = self.player[0] + 15
        self.rect[1] = self.player[1] + 15

    def update(self):

        speed = -20.
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= bullet_vector[0]
        self.rect.y -= bullet_vector[1]

spriteList = pygame.sprite.Group()

def makeBullet(displayInfo):
    bullet = Bullet(pygame.mouse.get_pos(), [displayInfo.current_w // 2 - 15, displayInfo.current_h // 2 - 15])
    spriteList.add(bullet)

def renderBullets(screen, displayInfo):
    for sprite in spriteList:
        if(sprite.rect[0] > displayInfo.current_w -100 or sprite.rect[1] > displayInfo.current_h-100 or sprite.rect[0] < 100 or sprite.rect[1] < 100):
            spriteList.remove(sprite)
        sprite.update()
    spriteList.draw(screen)





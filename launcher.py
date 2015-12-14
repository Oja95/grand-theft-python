import pygame
import time

class Option:

    hovered = False
    # Objekile antavad argumendid self-explainatory.
    # text - tekst
    # pos - optioni positisoon screeni suhtes
    # font - font object

    def __init__(self, text, pos, font, screen):
        self.menu_font = font
        self.screen = screen
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


def launcher(screen, displayInfo, murderCount=0, restart=False):
    menu_font = pygame.font.Font(None, 40)
    options = [Option("Uus mäng", (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 - 200), menu_font, screen),
               Option("Fullscreen", (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 - 150), menu_font, screen),
               Option("Sulge", (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 - 100), menu_font, screen),
               Option("WASD - movement", (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 + 50 ), menu_font, screen),
               Option("F - ingame fullscreen toggle", (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 + 100), menu_font, screen),
               Option("Esc - quit", (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 + 150), menu_font, screen)
               ]
    if(restart):
        status_font = pygame.font.Font(None, 60)
        options.append(Option("You dun' goofed m8. Zombied sõid su ära!", \
                    (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 - 400), status_font, screen))
        options.append(Option("Mõrvatud zombiesid: "+ str(murderCount), \
                    (displayInfo.current_w // 2 - 50, displayInfo.current_h // 2 - 350), status_font, screen))
    closed = False
    """
    menuImage = pygame.image.load("images/menu.png").convert()
    screen.blit(menuImage, (0,0))
    """
    while not closed:
        pygame.event.pump()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()
        key = pygame.key.get_pressed()
        if(key[pygame.K_ESCAPE]):
            pygame.quit()
            exit()
        if(key[pygame.K_f]):
            pygame.display.toggle_fullscreen()

        if(pygame.mouse.get_pressed() == (1,0,0)):  # Left mouse klikk
            for option in options:
                if(option.rect.collidepoint(pygame.mouse.get_pos())):
                    if(option.text == "Sulge"):
                        pygame.quit()
                        exit()
                    if(option.text == "Uus mäng"):
                        closed = True
                    if(option.text == "Fullscreen"):
                        pygame.display.toggle_fullscreen()
                        time.sleep(0.25)  # 0.25 sekki delay, et ühe klõpsuga mitut togglet ei tehta

        for option in options:
            if(option.rect.collidepoint(pygame.mouse.get_pos())):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        pygame.display.update()






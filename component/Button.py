import pygame.image
import pygame.transform


class Button:
    def __init__(self, func, size, pos):
        self.img = pygame.image.load(f"images/function/icon_{func}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(center=pos)
        self.state = False

    def show(self, screen: pygame.Surface):
        screen.blit(self.img, self.rect)

    def pressed(self, pos):
        if self.rect.collidepoint(pos):
            self.state = True
        else:
            self.state = False

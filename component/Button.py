import pygame.image
import pygame.transform


class Button:
    def __init__(self, func, size, pos):
        self.img = pygame.image.load(f"images/function/icon_{func}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(center=pos)
        self.state = False

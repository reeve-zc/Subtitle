import pygame
from setting import *
from component.Button import Button


class FloatingInterface:
    def __init__(self, size):
        self.rect = pygame.Rect(WIDTH / 2 - size[0] / 2, HEIGHT / 2 - size[1] / 2, size[0], size[1])
        self._bg = pygame.transform.scale(pygame.image.load(f"images/background/else/yellow_bg.png").convert_alpha(),
                                          size)
        self._btn_close = Button("close", (65, 65), ((WIDTH / 2) + (size[0] / 2) - size[0] * 0.165,
                                                     (HEIGHT / 2) - (size[1] / 2) + size[1] * 0.24))

    def show(self, screen: pygame.Surface):
        bg_filter = screen.copy().convert_alpha()
        bg_filter.fill((0, 0, 0, 50))
        screen.blit(bg_filter, (0, 0))
        screen.blit(self._bg, self.rect)
        self._btn_close.show(screen)

    @property
    def btn_close(self):
        return self._btn_close

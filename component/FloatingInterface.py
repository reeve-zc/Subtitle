import pygame
from setting import *
from component.Button import Button


class FloatingInterface():
    def __init__(self, width, height):
        self._height = height
        self._width = width
        self._bg = pygame.transform.scale(pygame.image.load(f"images/background/else/yellow_bg.png").convert_alpha(),
                                          (self._width, self._height))
        self._btn_close = Button("close", (65, 65),
                                 ((WIDTH / 2) + (self._width / 2) - 260, (HEIGHT / 2) - (self._height / 2) + 230))

    def show(self, screen: pygame.Surface):
        bg_filter = screen.copy().convert_alpha()
        bg_filter.fill((0, 0, 0, 50))
        screen.blit(bg_filter, (0, 0))
        screen.blit(self._bg, ((WIDTH / 2) - (self._width / 2), (HEIGHT / 2) - (self._height / 2)))
        self._btn_close.show(screen)



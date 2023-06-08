import os

import pygame.draw
import pygame.image
import pygame.transform

from setting import WIDTH, HEIGHT


class Background:
    def __init__(self, path="./images/background"):
        self._path = None
        self._bgList = None
        self._surface = None
        self.update_background(path)

        self._bg_img = None
        self._index = 0

        self._fps = 150
        self._fps_counter = pygame.USEREVENT

    def animation(self):
        self._index = (self._index + 1) % len(self._surface)
        self._bg_img = self._surface[self._index]

    def update_background(self, path):
        self._path = path
        self._bgList = list(filter(lambda x: 'png' in x, os.listdir(self._path)))
        self._bgList.sort(key=lambda x: (len(x), x))
        self._surface = [pygame.image.load("images/background/" + x).convert() for x in self._bgList]
        self._bg_img = self._surface[0]

    def load_bg_img(self, screen: pygame.Surface):
        self._bg_img = pygame.transform.scale(self._bg_img, (WIDTH, HEIGHT))

        bg_filter = screen.copy().convert_alpha()
        bg_filter.fill((0, 0, 0, 100))

        screen.blit(bg_filter, (0, 0))
        screen.blit(self._bg_img, (0, 0))
        screen.blit(bg_filter, (0, 0))

    @property
    def fps(self):
        return self._fps

    @property
    def fps_counter(self):
        return self._fps_counter

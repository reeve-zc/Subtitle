import pygame
import os
from setting import *
from component.Button import Button
from component.FloatingInterface import FloatingInterface


class PlayList():
    def __init__(self):
        self._state = False
        self._btn_playlist = Button("playlist", (80, 80), (190, 120))
        self._floatinginterface = FloatingInterface(1600,1000)

    def playlist_pressed(self, pos):
        self._btn_playlist.pressed(pos)
        self.close_btn_pressed(pos)

    def playlist_compressed(self):
        if self._btn_playlist.state:
            self._state = True
            self._btn_playlist.state = False

    def close_btn_pressed(self, pos):
        if self._floatinginterface._btn_close.rect.collidepoint(pos):
            self._state = False




    def show(self, screen: pygame.Surface):
        self._btn_playlist.show(screen)
        if self._state:
            self._floatinginterface.show(screen)
        None

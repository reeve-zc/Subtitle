import pygame
import os
from setting import *
from component.Button import Button
from component.FloatingInterface import FloatingInterface


class PlayList:
    def __init__(self):
        self._state = False
        self._btn_playlist = Button("playlist", (80, 80), (190, 120))
        self._floating_interface = FloatingInterface((1600, 1000))
        self._active = True

    def pressed(self, pos):
        if self._active:
            self._btn_playlist.pressed(pos)
            self._floating_interface.btn_close.pressed(pos)

    def compressed(self):
        self.playlist_btn_compressed()
        self.close_btn_compressed()
        return self._state

    def playlist_btn_compressed(self):
        if self._btn_playlist.state:
            self._btn_playlist.state = False
            self._state = True

    def close_btn_compressed(self):
        if self._floating_interface.btn_close.state:
            self._floating_interface.btn_close.state = False
            self._state = False

    def show(self, screen: pygame.Surface):
        if self._state:
            self._floating_interface.show(screen)

    @property
    def btn_playlist(self):
        return self._btn_playlist

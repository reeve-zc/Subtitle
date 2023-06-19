import pygame
import os

from component.Button import Button
from component.FloatingInterface import FloatingInterface
from component.CardView import SongCardView


class PlayList:
    def __init__(self):
        self._btn_playlist = Button("playlist", (80, 80), (190, 120))
        self._btn_next = Button("next", (60, 60), (1130, 150))
        self._floating_interface = FloatingInterface((1200, 1200))

        self._index = 0
        self._songs = list(filter(lambda x: 'mp3' in x, os.listdir('./musics')))
        self._song_view = SongCardView(self._songs)

        self._state = False
        self._active = True

    def pressed(self, pos):
        if self._active:
            self._btn_next.pressed(pos)
            self._btn_playlist.pressed(pos)
            self._floating_interface.btn_close.pressed(pos)
            if self._state:
                self._song_view.pressed(pos)

    def compressed(self):
        self.playlist_btn_compressed()
        self.close_btn_compressed()
        if self.next_btn_compressed():
            return self._state, self._songs[self._index]

        index = self._song_view.compressed()
        if index is not None:
            song = self._songs[index]
            self._index = index
        else:
            song = None
        return self._state, song

    def mov(self, pos):
        if self._state:
            self._song_view.mov(pos)

    def playlist_btn_compressed(self):
        if self._btn_playlist.state:
            self._btn_playlist.state = False
            self._songs = list(filter(lambda x: 'mp3' in x, os.listdir('./musics')))
            self._song_view.update_song_list(self._songs)
            self._state = True

    def next_btn_compressed(self):
        if self._btn_next.state:
            self._btn_next.state = False
            self._index = (self._index + 1) % len(self._songs)
            return True

    def close_btn_compressed(self):
        if self._floating_interface.btn_close.state:
            self._floating_interface.btn_close.state = False

            self._state = False

    def show(self, screen: pygame.Surface):
        self._btn_next.show(screen)
        if self._state:
            self._floating_interface.show(screen)
            self._song_view.show(screen)

    @property
    def btn_playlist(self):
        return self._btn_playlist

    @property
    def songs(self):
        return self._songs

import sys
import pygame

from setting import *

from component.Background import Background
from component.Button import Button
from component.Player import Player
from component.Search import Search
from component.CardView import TodoCardView
from component.PlayList import PlayList
from component.Timer import Timer


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Subtitle')
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.search = Search()
        self.playlist = PlayList()
        self.background = Background()
        self.todolist = TodoCardView()
        self.timer = Timer()

    def run(self):
        btn_setting = Button("setting", (82, 82), (120, 120))
        btn_skull_nor = Button("skull_count", (300, 61.391), (240, 698))

        pygame.time.set_timer(pygame.USEREVENT, self.background.fps)
        pygame.time.set_timer(pygame.USEREVENT + 1, self.player.song_name.fps)
        pygame.time.set_timer(pygame.USEREVENT + 2, self.timer.fps)
        pygame.time.set_timer(pygame.USEREVENT + 3, self.search.input.fps)
        pygame.time.set_timer(pygame.USEREVENT + 3, self.todolist.fps)

        t = pygame.time.get_ticks()
        get_ticks_last_frame = t

        self.player.change_song("musics/" + self.playlist.songs[0])

        while True:
            t = pygame.time.get_ticks()
            delta_time = (t - get_ticks_last_frame) / 1000.0
            get_ticks_last_frame = t

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.todolist.store_cards()
                    pygame.quit()
                    sys.exit()

                if event.type == self.background.fps_counter:
                    self.background.animation()

                if event.type == self.player.song_name.fps_counter:
                    self.player.song_name.animation()

                if event.type == self.timer.fps_counter:
                    if self.timer.counting:
                        self.timer.animation()

                if event.type == self.search.input.fps_counter:
                    self.search.input.animation()

                if event.type == self.todolist.fps_counter:
                    self.todolist.animation()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.pressed(event.pos)
                    self.timer.pressed(event.pos)
                    self.playlist.pressed(event.pos)
                    self.todolist.pressed(event.pos)
                    self.search.pressed(event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.compressed()
                    self.todolist.compressed()
                    self.timer.compressed()
                    state, song = self.playlist.compressed()

                    if self.search.compressed():
                        self.player._active = False
                        self.todolist._active = False
                        self.playlist._active = False
                        self.timer._active = False
                    elif state:
                        self.player._active = False
                        self.todolist._active = False
                        self.search._active = False
                        self.timer._active = False
                    else:
                        self.player._active = True
                        self.todolist._active = True
                        self.search._active = True
                        self.playlist._active = True
                        self.timer._active = True

                    if song:
                        self.player.change_song("musics/" + song)

                if event.type == pygame.MOUSEMOTION:
                    # print(event.pos)
                    self.playlist.mov(event.pos)
                    self.player.mov(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.todolist.key_down(event)
                    if self.search.key_down(event) or self.playlist.key_down(event):
                        self.player._active = True
                        self.todolist._active = True
                        self.search._active = True
                        self.playlist._active = True
                        self.timer._active = True

            self.background.load_bg_img(self.screen)

            btn_setting.show(self.screen)
            btn_skull_nor.show(self.screen)

            self.timer.show(self.screen)
            self.player.show(self.screen, delta_time)
            self.todolist.show(self.screen)

            self.search.btn_search.show(self.screen)
            self.playlist.btn_playlist.show(self.screen)
            self.playlist.show(self.screen)
            self.search.show(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

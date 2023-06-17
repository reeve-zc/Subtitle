import sys
import pygame

from setting import *

from component.Background import Background
from component.Button import Button
from component.Player import Player
from component.Search import Search
from component.CardView import TodoCardView
from component.PlayList import PlayList
from component.Card import Card


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
        self.todo_list = TodoCardView()

    def run(self):
        btn_music = Button("setting", (82, 82), (120, 120))
        btn_next = Button("next", (60, 60), (1130, 150))

        pygame.time.set_timer(pygame.USEREVENT, self.background.fps)
        pygame.time.set_timer(pygame.USEREVENT + 1, self.player.song_name.fps)
        pygame.time.set_timer(pygame.USEREVENT + 3, self.search.input.fps)

        t = pygame.time.get_ticks()
        get_ticks_last_frame = t

        self.player.change_song(
            "musics/Dua Lipa - Levitating Featuring DaBaby (Official Music Video).mp3")

        while True:
            t = pygame.time.get_ticks()
            delta_time = (t - get_ticks_last_frame) / 1000.0
            get_ticks_last_frame = t

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.background.fps_counter:
                    self.background.animation()

                if event.type == self.player.song_name.fps_counter:
                    self.player.song_name.animation()

                if event.type == self.search.input.fps_counter:
                    self.search.input.animation()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.player_pressed(event.pos)
                    self.playlist.playlist_pressed(event.pos)
                    if self.search.search_pressed(event.pos):
                        self.player._active = False
                    else:
                        self.player._active = True


                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.player_compressed()
                    self.search.search_compressed()
                    self.playlist.playlist_compressed()

                if event.type == pygame.MOUSEMOTION:
                    print(event.pos)
                    self.player.player_mov(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.search.search_bar_key_down(event)

            self.background.load_bg_img(self.screen)


            btn_music.show(self.screen)
            btn_next.show(self.screen)

            self.player.show(self.screen, delta_time)
            self.todo_list.show(self.screen)
            self.search.show(self.screen)
            self.playlist.show(self.screen)
            # self.card.show(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

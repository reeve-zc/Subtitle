import sys
import pygame
from setting import *

from component.Background import Background
from component.Button import Button
from component.Player import Player


class Search:
    def __init__(self):
        self._btn_search = Button("search", (90, 90), (270, 120))
        self._btn_close = Button("close", (65, 65), (935, 180))
        self._surface = pygame.image.load(f"images/background/else/yellow_bg.png").convert_alpha()
        self._surface = pygame.transform.scale(self._surface, (SEARCH_SURFACE_WIDTH, SEARCH_SURFACE_HEIGHT))
        self._state = False
        self._active = True

    def search_pressed(self, pos):
        if self._active:
            self.search_btn_pressed(pos)
            self.close_btn_pressed(pos)
            return self._state

    def search_btn_pressed(self, pos):
        if self._btn_search.rect.collidepoint(pos):
            self._state = True

    def close_btn_pressed(self, pos):
        if self._btn_close.rect.collidepoint(pos):
            self._state = False

    def show(self, screen: pygame.Surface):
        screen.blit(self._btn_search.img, self._btn_search.rect)

        if self._state:
            bg_filter = screen.copy().convert_alpha()
            bg_filter.fill((0, 0, 0, 50))
            screen.blit(bg_filter, (0, 0))
            screen.blit(self._surface, (SEARCH_SURFACE_X, SEARCH_SURFACE_Y))
            screen.blit(self._btn_close.img, self._btn_close.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Subtitle')
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.search = Search()
        self.background = Background()

    def run(self):
        btn_music_list = Button("musiclist", (80, 80), (120, 120))
        btn_music = Button("music", (80, 80), (190, 120))
        btn_next = Button("next", (60, 60), (1130, 150))

        pygame.time.set_timer(pygame.USEREVENT, self.background.fps)
        pygame.time.set_timer(pygame.USEREVENT + 1, self.player.song_name.fps)

        t = pygame.time.get_ticks()
        get_ticks_last_frame = t

        self.player.change_song(
            "musics/告五人 Accusefive 【愛人錯過 Somewhere in time】Official Music Video.mp3")

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.player_pressed(event.pos)
                    if self.search.search_pressed(event.pos):
                        self.player._active = False
                    else:
                        self.player._active = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.player_compressed()

                if event.type == pygame.MOUSEMOTION:
                    self.player.player_mov(event.pos)

            self.background.load_bg_img(self.screen)

            self.screen.blit(btn_music_list.img, btn_music_list.rect)
            self.screen.blit(btn_music.img, btn_music.rect)
            self.screen.blit(btn_next.img, btn_next.rect)

            self.player.show(self.screen, delta_time)
            self.search.show(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

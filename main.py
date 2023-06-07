import sys
import pygame
from setting import *

from component.Background import Background
from component.Button import Button
from component.Player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Subtitle')
        self.clock = pygame.time.Clock()
        self.player = Player()
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
                    self.player.song_name.show_name()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.play_bar_pressed(event.pos)
                    self.player.sound_bar_pressed(event.pos)
                    self.player.play_btn_pressed(event.pos)
                    self.player.reset_btn_pressed(event.pos)
                    self.player.volume_btn_pressed(event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.play_btn_compressed()
                    self.player.play_bar_compressed()
                    self.player.sound_bar_compressed()
                    self.player.reset_btn_compressed()

                if event.type == pygame.MOUSEMOTION:
                    self.player.play_bar_mov(event.pos)
                    self.player.sound_bar_mov(event.pos)

            self.background.load_bg_img(self.screen)

            self.screen.blit(btn_music_list.img, btn_music_list.rect)
            self.screen.blit(btn_music.img, btn_music.rect)
            self.screen.blit(btn_next.img, btn_next.rect)

            self.player.showing(self.screen, delta_time)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

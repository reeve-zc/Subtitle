import sys
import os

import pygame.draw
from pydub import AudioSegment

from audio import *


class PlayBackBar:
    def __init__(self):
        self._size = 14
        self._top = Y_START + 50 - self._size / 2
        self._left = X_START - self._size / 2
        self._rect = pygame.Rect(self._left, self._top, self._size, self._size)
        self._duration = 0
        self._time = 0
        self._state = False

    def reset(self):
        self._duration = 0
        self._time = 0
        self._state = False
        self._top = Y_START + 50 - self._size / 2
        self._left = X_START - self._size / 2

    def get_time(self):
        delta_x = self._left + self._size / 2 - X_START
        self._time = delta_x / (LENGTH / self._duration)

    def moving(self, time):
        delta_x = time * LENGTH / self._duration
        self._left = min(X_START - self._size / 2 + delta_x, X_END)

    def set_pos(self, pos):
        mx, _ = pos
        mx = clamp(X_START, X_END, mx)
        self._left = mx - self._size / 2
        return self.get_time()

    def show(self, screen):
        if self._state:
            size = self._size + 2
            top = self._top - 1
            left = self._left - 1
        else:
            size = self._size
            top = self._top
            left = self._left

        pygame.draw.line(screen, DEFAULT_COLOR, (X_START, Y_START + 50), (X_END, Y_END + 50), width=LINE_WIDTH)
        pygame.draw.line(screen, DEFAULT_COLOR, (X_START, Y_START + 50), (self._left + self._size / 2, Y_END + 50),
                         width=LINE_WIDTH + 2)
        self._rect = pygame.Rect(left, top, size, size)
        pygame.draw.rect(screen, DEFAULT_COLOR, self._rect, border_radius=int(size / 2))

    @property
    def rect(self):
        return self._rect

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def duration(self):
        return self._duration

    @property
    def time(self):
        return self._time


class Button:
    def __init__(self, func, size, pos):
        self.img = pygame.image.load(f"images/function/icon_{func}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(center=pos)
        self.state = False


class SongName:
    def __init__(self, font="fonts/AA桔梗少女V1.3.TTF", font_size=40, color=DEFAULT_COLOR):
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.name = None
        self.surface = None
        self.x = 0

    def reset(self):
        self.name = None
        self.surface = None
        self.x = 0

    def update_song(self, song):
        self.name = self.font.render("   " + song + "   ", True, self.color)
        self.surface = pygame.Surface((572, self.name.get_height()), flags=pygame.HWSURFACE)
        self.surface = self.surface.convert_alpha()

    def show_name(self):
        self.surface.fill((255, 255, 255, 0))
        self.x -= 1
        if self.x < -self.name.get_width():
            self.x = 0

        self.surface.blit(self.name, (self.x, 0))
        self.surface.blit(self.name, (self.x + self.name.get_width(), 0))


class Player:
    def __init__(self, setting=DEFAULT_PLAYER_SETTING):
        pygame.mixer.init()
        self._music = pygame.mixer.music
        self._playing_pos = 0
        self._last = False
        self._playing = False
        self._end = False
        self._song = None
        self._song_name = SongName()
        self._audio = Audio()
        self._playback_bar = PlayBackBar()
        self._setting = setting

    def change_song(self, filename):
        self.reset()
        self._song = filename
        self._song_name.update_song(filename[7:])
        self._playback_bar._duration = AudioSegment.from_mp3(self._song).duration_seconds

        self.start()
        self.pause()

    def reset(self):
        self._playing_pos = 0
        self._song = None
        self._last = False
        self._playing = False
        self._end = False
        self._playback_bar.reset()
        self._song_name.reset()

    def start(self):
        self._audio.load(self._song)
        self._music.load(self._song)
        self._music.play(0)

    def restart(self):
        if self._end:
            self._playing = True

        self._end = False
        self._playing_pos = 0
        self._music.play(0)
        self.playback_bar.set_pos((0, 0))

        if not self._playing:
            self.pause()

    def check_restart(self):
        if self._end:
            self.restart()

    def reverse_state(self):
        self._playing = not self._playing

    def play_btn_pressed(self):
        self.reverse_state()
        self.check_restart()

    def play_btn_compressed(self):
        if self._playing:
            self.unpause()
        else:
            self.pause()

    def pause(self):
        self._music.pause()
        self._playing = False

    def unpause(self):
        self._music.unpause()
        self._playing = True

    def stop(self):
        self._music.stop()

    def set_time(self, time):
        if time >= self.playback_bar.duration:
            time = self.playback_bar.duration
        else:
            self._end = False

        self._playing_pos = self._music.get_pos() - time * 1000
        self._music.set_pos(time)
        if not self._playing:
            self._music.pause()

    def get_time(self, delta_time):
        time = (self._music.get_pos() - self._playing_pos) / 1000

        if time + delta_time >= self.playback_bar.duration:
            time = self.playback_bar.duration
            self._end = True
            self._playing = False

        return time

    def get_volume(self):
        return self._music.get_volume()

    def set_volume(self, value):
        return self._music.set_volume(value)

    def add_song(self, song):
        self._music.queue(song)

    def showing(self, screen, delta_time):
        self._song_name.show_name()
        screen.blit(self._song_name.surface, (X_START, Y_START + 100))
        self._audio.update_bars(screen, delta_time, self.get_time(delta_time))

        if self.playing:
            self._playback_bar.moving(self.get_time(delta_time))
        self._playback_bar.show(screen)

    @property
    def playing(self):
        return self._playing

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, value):
        self._last = value

    @property
    def end(self):
        return self._end

    @property
    def playback_bar(self):
        return self._playback_bar


class Background:
    def __init__(self, path="./images/background"):
        self._path = None
        self._bgList = None
        self._surface = None
        self.update_background(path)

        self._bg_img = None
        self._index = 0

        self.fps = 150
        self.fps_counter = pygame.USEREVENT

    def animation(self):
        self._index = (self._index + 1) % len(self._surface)
        self._bg_img = self._surface[self._index]

    def update_background(self, path):
        self._path = path
        self._bgList = list(filter(lambda x: 'png' in x, os.listdir(self._path)))
        self._bgList.sort(key=lambda x: (len(x), x))
        self._surface = [pygame.image.load("images/background/" + x).convert() for x in self._bgList]
        self._bg_img = self._surface[0]

    def load_bg_img(self, screen):
        self._bg_img = pygame.transform.scale(self._bg_img, (WIDTH, HEIGHT))

        bg_filter = screen.copy().convert()
        pygame.draw.rect(bg_filter, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        bg_filter.set_alpha(100)

        screen.blit(self._bg_img, (0, 0))
        screen.blit(bg_filter, (0, 0))


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
        btn_play = Button("play", (75, 75), (1015, 150))
        btn_pause = Button("pause", (65, 65), (1015, 150))
        btn_reset = Button("reset", (60, 60), (1070, 150))
        btn_next = Button("next", (60, 60), (1130, 150))

        pygame.time.set_timer(pygame.USEREVENT, self.background.fps)

        t = pygame.time.get_ticks()
        get_ticks_last_frame = t

        self.player.change_song("musics/【完整版】鈴芽之旅 主題曲 - RADWIMPS - すずめ (feat. 十明)『中日字幕』.mp3")

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if btn_pause.rect.collidepoint(pos):
                        self.player.play_btn_pressed()

                    if btn_reset.rect.collidepoint(pos):
                        btn_reset.state = True

                    if self.player.playback_bar.rect.collidepoint(pos):
                        self.player.last = self.player.playing
                        self.player.pause()
                        self.player.playback_bar.state = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.play_btn_compressed()

                    if btn_reset.state:
                        self.player.restart()
                        btn_reset.state = False

                    if self.player.playback_bar.state:
                        self.player.playback_bar.state = False
                        if self.player.last:
                            if not self.player.end:
                                self.player.unpause()

                if event.type == pygame.MOUSEMOTION:
                    if self.player.playback_bar.state:
                        self.player.playback_bar.set_pos(event.pos)
                        self.player.set_time(self.player.playback_bar.time)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.change_song(
                            "musics/Dua Lipa - Levitating Featuring DaBaby (Official Music Video).mp3")

            self.background.load_bg_img(self.screen)

            self.screen.blit(btn_music_list.img, btn_music_list.rect)
            self.screen.blit(btn_music.img, btn_music.rect)
            self.screen.blit(btn_reset.img, btn_reset.rect)
            self.screen.blit(btn_next.img, btn_next.rect)

            if self.player.playing:
                self.screen.blit(btn_pause.img, btn_pause.rect)
            else:
                self.screen.blit(btn_play.img, btn_play.rect)

            self.player.showing(self.screen, delta_time)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

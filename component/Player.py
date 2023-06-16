import pygame.draw
import pygame.font
import pygame.mixer
from pydub import AudioSegment

from component.Bar import SoundBar, PlayBackBar
from component.Button import Button
from component.Audio import Audio
from setting import *


class Player:
    def __init__(self, setting=DEFAULT_PLAYER_SETTING):
        pygame.mixer.init()
        self._music = pygame.mixer.music

        self._playing_pos = 0
        self._volume = 50.0

        self._last = False
        self._playing = False
        self._end = False
        self._active = True

        self._song = None

        self._song_name = SongName()
        self._audio = Audio()
        self._sound_bar = SoundBar()
        self._playback_bar = PlayBackBar()
        self._setting = setting

        self._btn_play = Button("play", (75, 75), (1015, 150))
        self._btn_pause = Button("pause", (65, 65), (1015, 150))
        self._btn_reset = Button("reset", (60, 60), (1070, 150))

    def change_song(self, filename):
        self._reset()
        self._song = filename
        self._song_name.update_song(filename[7:])
        self._playback_bar.duration = AudioSegment.from_mp3(self._song).duration_seconds
        self._set_volume()

        self._start()
        self._pause()

    def player_pressed(self, pos):
        if self._active:
            self._play_bar_pressed(pos)
            self._sound_bar_pressed(pos)
            self._btn_pause.pressed(pos)
            self._btn_reset.pressed(pos)
            self._sound_bar.btn_volume.pressed(pos)

    def player_compressed(self):
        self._play_btn_compressed()
        self._play_bar_compressed()
        self._sound_bar_compressed()
        self._reset_btn_compressed()
        self._volume_btn_compressed()

    def player_mov(self, pos):
        self._play_bar_mov(pos)
        self._sound_bar_mov(pos)

    def show(self, screen: pygame.Surface, delta_time):
        self._volume = self._sound_bar.get_pos()
        self._set_volume()
        self._audio.update_bars(screen, delta_time, self._get_time(delta_time))

        if self._playing:
            self._btn_pause.show(screen)
            self._playback_bar.moving(self._get_time(delta_time))
        else:
            self._btn_play.show(screen)

        self._btn_reset.show(screen)

        self._sound_bar.show(screen)
        self._playback_bar.show(screen)
        self._song_name.show(screen)

    def _reset(self):
        self._playing_pos = 0
        self._song = None
        self._last = False
        self._playing = False
        self._end = False
        self._playback_bar.reset()
        self._song_name.reset()

    def _start(self):
        self._audio.load(self._song)
        self._music.load(self._song)
        self._music.play(0)

    def _restart(self):
        if self._end:
            self._playing = True

        self._end = False
        self._playing_pos = 0
        self._music.play(0)
        self._playback_bar.set_pos((0, 0))

        if not self._playing:
            self._pause()

    def _check_restart(self):
        if self._end:
            self._restart()

    def _reverse_state(self):
        self._playing = not self._playing

    def _volume_btn_compressed(self):
        if self._sound_bar.btn_volume.state:
            self._sound_bar.reverse_state()
            self._sound_bar.btn_volume.state = False

    def _play_btn_compressed(self):
        if self._btn_pause.state:
            self._reverse_state()
            self._check_restart()
            self._btn_pause.state = False

        if self._playing:
            self._unpause()
        else:
            self._pause()

    def _reset_btn_compressed(self):
        if self._btn_reset.state:
            self._restart()
            self._btn_reset.state = False

    def _play_bar_pressed(self, pos):
        if self._playback_bar.rect.collidepoint(pos) or self._playback_bar.line_rect.collidepoint(pos):
            self._set_time(self._playback_bar.set_pos(pos))
            self._last = self._playing
            self._pause()
            self._playback_bar.state = True

    def _play_bar_compressed(self):
        if self._playback_bar.state:
            self._playback_bar.state = False
            if self._last:
                if not self._end:
                    self._unpause()

    def _play_bar_mov(self, pos):
        if self._playback_bar.state:
            self._set_time(self._playback_bar.set_pos(pos))

    def _sound_bar_pressed(self, pos):
        if self._sound_bar.rect.collidepoint(pos) or self._sound_bar.line_rect.collidepoint(pos):
            self._sound_bar.set_pos(pos)
            self._sound_bar.state = True

    def _sound_bar_compressed(self):
        if self._sound_bar.state:
            self._sound_bar.state = False

    def _sound_bar_mov(self, pos):
        if self._sound_bar.state:
            self._sound_bar.set_pos(pos)

    def _pause(self):
        self._music.pause()
        self._playing = False

    def _unpause(self):
        self._music.unpause()
        self._playing = True

    def _stop(self):
        self._music.stop()

    def _set_time(self, time):
        if self._end:
            self._playing_pos = 0
            self._music.play(0)
        if time >= self._playback_bar.duration:
            time = self._playback_bar.duration
        else:
            self._end = False

        self._playing_pos = self._music.get_pos() - time * 1000
        self._music.set_pos(time)
        if not self._playing:
            self._music.pause()

    def _get_time(self, delta_time):
        time = (self._music.get_pos() - self._playing_pos) / 1000

        if time + delta_time >= self._playback_bar.duration:
            time = self._playback_bar.duration
            self._end = True
            self._playing = False

        return time

    def _get_volume(self):
        return self._music.get_volume()

    def _set_volume(self):
        self._music.set_volume(self._volume / 100)

    def _add_song(self, song):
        self._music.queue(song)

    @property
    def song_name(self):
        return self._song_name


class SongName:
    def __init__(self, font_size=40):
        self.font = pygame.font.Font("fonts/AA桔梗少女V1.3.TTF", font_size)
        self.name = None
        self.surface = None
        self.x = 0

        self._fps = 10
        self._fps_counter = pygame.USEREVENT + 1

    def reset(self):
        self.name = None
        self.surface = None
        self.x = 0

    def update_song(self, song):
        self.name = self.font.render("   " + song + "   ", True, DEFAULT_COLOR)
        self.surface = pygame.Surface((572, self.name.get_height()), flags=pygame.HWSURFACE).convert_alpha()

    def animation(self):
        self.x -= 1
        if self.x < -self.name.get_width():
            self.x = 0

    def show(self, screen: pygame.Surface):
        self.surface.fill((255, 255, 255, 0))

        self.surface.blit(self.name, (self.x, 0))
        self.surface.blit(self.name, (self.x + self.name.get_width(), 0))
        screen.blit(self.surface, (X_START, SONG_NAME_Y))

    @property
    def fps(self):
        return self._fps

    @property
    def fps_counter(self):
        return self._fps_counter

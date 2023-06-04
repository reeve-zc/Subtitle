import librosa.display
import numpy as np
import pygame

from setting import *


def clamp(min_value, max_value, value):
    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioAnalyzer:

    def __init__(self):
        self.frequencies_index_ratio = 0  # array for frequencies
        self.time_index_ratio = 0  # array of time periods
        self.spectrogram = None  # a matrix that contains decibel values according to frequency and time indexes

    def load(self, filename):
        time_series, sample_rate = librosa.load(filename)  # getting information from the file

        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048 * 4))

        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

        frequencies = librosa.core.fft_frequencies(n_fft=2048 * 4)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512,
                                            n_fft=2048 * 4)

        self.time_index_ratio = len(times) / times[len(times) - 1]

        self.frequencies_index_ratio = len(frequencies) / frequencies[len(frequencies) - 1]

    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq * self.frequencies_index_ratio)][int(target_time * self.time_index_ratio)]

        # returning the current decibel according to the indexes which found by binary search
        # return self.spectrogram[bin_search(self.frequencies, freq), bin_search(self.times, target_time)]


class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height) / 0.1

        self.height += speed * dt

        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))


class AverageAudioBar(AudioBar):

    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)

        self.rng = rng

        self.avg = 0

    def update_all(self, dt, time, analyzer):
        self.avg = 0

        for i in self.rng:
            self.avg += analyzer.get_decibel(time, i)

        self.avg /= len(self.rng)
        self.update(dt, self.avg)


class Music:
    def __init__(self, screen):
        self._analyzer = AudioAnalyzer()
        self._song = ""
        self._screen = screen

        self._bars = []
        self._bar_height = (HEIGHT / 2) - (BAR_MAX_HEIGHT / 2)
        self.audio_init()

    def audio_init(self):
        freq_groups = [BASS, HEAVY_AREA, LOW_MIDS, HIGH_MIDS]

        tmp_bars = []
        length = 0

        for group in freq_groups:
            g = []
            s = group["stop"] - group["start"]
            count = group["count"]
            reminder = s % count
            step = int(s / count)
            rng = group["start"]

            for i in range(count):
                if reminder > 0:
                    reminder -= 1
                    arr = np.arange(start=rng, stop=rng + step + 2)
                    rng += step + 3
                else:
                    arr = np.arange(start=rng, stop=rng + step + 1)
                    rng += step + 2

                g.append(arr)
                length += 1
            tmp_bars.append(g)

        w = BAR_START
        for g in tmp_bars:
            gr = []
            for c in g:
                gr.append(AverageAudioBar(w, self._bar_height, c, color=BAR_DEFAULT_COLOR,
                                          width=BAR_WIDTH, max_height=BAR_MAX_HEIGHT))
                w += BAR_WIDTH + SPACE
            self._bars.append(gr[0: 20])

    def music_start(self):
        pygame.mixer.music.load(self._song)
        pygame.mixer.music.play(0)

    def change_song(self, song):
        self._song = song
        self._analyzer.load(self._song)

    def update_bars(self, delta_time):

        for b1 in self._bars:
            for b in b1:
                b.update_all(delta_time, pygame.mixer.music.get_pos() / 1000.0, self._analyzer)
        for b1 in self._bars:
            for b in b1:
                x_start = BAR_START - 30
                y_start = self._bar_height + BAR_MAX_HEIGHT
                x_end = BAR_START + (BAR_WIDTH + SPACE) * 32 + 30 - SPACE
                y_end = self._bar_height + BAR_MAX_HEIGHT

                b.render(self._screen)
                pygame.draw.line(self._screen, BAR_DEFAULT_COLOR, (x_start, y_start), (x_end, y_end), width=LINE_WIDTH)
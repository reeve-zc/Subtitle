import librosa
import numpy as np
import pygame

from utils.common import clamp
from setting import *


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

    def update_all(self, dt, time, analyzer, color):
        self.avg = 0
        self.color = color

        for i in self.rng:
            self.avg += analyzer.get_decibel(time, i)

        self.avg /= len(self.rng)
        self.update(dt, self.avg)


class Audio:
    def __init__(self):
        self._analyzer = AudioAnalyzer()
        self._bars = []
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
                gr.append(AverageAudioBar(w, BAR_HEIGHT + 20, c, color=DEFAULT_COLOR,
                                          width=BAR_WIDTH, max_height=BAR_MAX_HEIGHT))
                w += BAR_WIDTH + SPACE
            self._bars.append(gr[0: 20])

    def update_bars(self, screen, delta_time, pos, color=DEFAULT_COLOR):

        for b1 in self._bars:
            for b in b1:
                b.update_all(delta_time, pos, self._analyzer, color)
        for b1 in self._bars:
            for b in b1:
                b.render(screen)
                pygame.draw.line(screen, DEFAULT_COLOR, (X_START, Y_START), (X_END, Y_END), width=LINE_WIDTH)

    def load(self, song):
        self._analyzer.load(song)

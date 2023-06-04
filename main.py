import sys
import os

from audio import *


class Background:
    def __init__(self, path="./images/background"):
        self._path = None
        self._bgList = None
        self._bg_len = None
        self.update_background(path)

    @property
    def bg_len(self):
        return self._bg_len

    def update_background(self, path):
        self._path = path
        self._bgList = list(filter(lambda x: 'png' in x, os.listdir(self._path)))
        self._bgList.sort(key=lambda x: (len(x), x))
        self._bg_len = len(self._bgList)

    def load_bg_img(self, screen, index):
        bg_img = pygame.image.load("images/background/" + self._bgList[index])
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

        bg_filter = screen.copy().convert()
        pygame.draw.rect(bg_filter, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        bg_filter.set_alpha(100)

        screen.blit(bg_img, (0, 0))
        screen.blit(bg_filter, (0, 0))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Subtitle')
        self.clock = pygame.time.Clock()
        self.music = Audio()
        self.background = Background()

    def run(self):
        t = pygame.time.get_ticks()
        get_ticks_last_frame = t

        index = 0
        self.music.change_song("musics/music.mp3")
        self.music.music_start()

        while True:
            t = pygame.time.get_ticks()
            delta_time = (t - get_ticks_last_frame) / 1000.0
            get_ticks_last_frame = t

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.background.load_bg_img(self.screen, index)
            index = (index + 1) % self.background.bg_len

            self.music.update_bars(self.screen, delta_time)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

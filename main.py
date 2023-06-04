import sys
import os

from audio import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Subtitle')
        self.clock = pygame.time.Clock()
        self.music = Music()
        self.bgList = list(filter(lambda x: 'png' in x, os.listdir('./images/background')))

    def run(self):
        t = pygame.time.get_ticks()
        get_ticks_last_frame = t

        index = 0
        self.bgList.sort(key=lambda x: (len(x), x))
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

            bg_img = pygame.image.load("images/background/" + self.bgList[index])
            bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
            index = (index + 1) % len(self.bgList)

            bg_filter = self.screen.copy().convert()
            pygame.draw.rect(bg_filter, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
            bg_filter.set_alpha(100)

            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(bg_filter, (0, 0))
            self.music.update_bars(self.screen, delta_time)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()

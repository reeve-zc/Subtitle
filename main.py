import pygame
import sys

from setting import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Subtitle')
        self.clock = pygame.time.Clock()
        self.index = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            bg_img = pygame.image.load(f'images/background/{self.index}.gif')
            bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
            self.screen.blit(bg_img, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)
            self.index = (self.index + 1) % 49


if __name__ == '__main__':
    game = Game()
    game.run()

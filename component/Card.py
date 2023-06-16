import pygame

from setting import *


class Card:
    def __init__(self, text, size, font_size, pos, padding=20):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.border = pygame.Rect(pos[0] - 3, pos[1] - 3, size[0] + 6, size[1] + 6)
        self.padding = padding
        self.pos = pos

        self.font = pygame.font.Font("fonts/紅夜角新書 PRO M (20180109).OTF", font_size)
        self.text = text

        self.select = False
        self.state = False

    def update(self, pos):
        self.rect.topleft = pos
        self.border.topleft = pos[0] - 3, pos[1] - 3

    def pressed(self, pos):
        if self.rect.collidepoint(pos):
            self.state = True
        else:
            self.select = False

    def compressed(self):
        if self.state:
            self.select = not self.select
            self.state = False

    def show_text(self, screen):
        max_width = self.rect.right - self.padding - 2
        x, y = self.rect.left + self.padding, self.rect.centery

        for word in self.text:
            word_surface = self.font.render(word, True, (0, 0, 0))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                screen.blit(self.font.render('...', True, (0, 0, 0)), (x, y - word_height / 2))
                break

            screen.blit(word_surface, (x, y - word_height / 2))
            x += word_width

    def show(self, screen: pygame.Surface):
        pygame.draw.rect(screen, DEFAULT_COLOR, self.rect, border_radius=20)
        if self.select:
            pygame.draw.rect(screen, DEFAULT_COLOR_SELECT, self.border, border_radius=22, width=3)
        self.show_text(screen)

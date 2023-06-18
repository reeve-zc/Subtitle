import pygame
import pyperclip

from setting import *
from component.Input import CardInput


class Card:
    def __init__(self, size, pos, padding=20):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.border = pygame.Rect(pos[0] - 3, pos[1] - 3, size[0] + 6, size[1] + 6)
        self.padding = padding

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

    def show(self, screen: pygame.Surface):
        pygame.draw.rect(screen, DEFAULT_COLOR, self.rect, border_radius=20)
        if self.select:
            pygame.draw.rect(screen, DEFAULT_COLOR_SELECT, self.border, border_radius=22, width=3)


class TodoCard(Card):
    def __init__(self, size, pos, font_size, font='Andale Mono.ttf', padding=20):
        super().__init__(size, pos, padding)
        pos = pos[0], pos[1] + size[1] / 2
        self.input = CardInput(font, pos, 10, font_size, length=15)

    def modify(self):
        self.input.state = True

    def get_text(self):
        return self.input.word

    def pressed(self, pos):
        super().pressed(pos)
        if not self.state:
            self.input.state = False
            self.input.enter()

    def compressed(self):
        super().compressed()

    def set_pos(self, pos):
        self.rect.topleft = pos
        self.border.topleft = pos[0] - 3, pos[1] - 3
        self.input.text.rect.midleft = self.rect.left + self.input.word_x, self.rect.centery

    def card_key_down(self, event: pygame.event):
        if self.input.state:
            if event.key == pygame.K_RETURN:
                self.input.enter()
                self.input.state = self.select = False
            elif event.key == pygame.K_BACKSPACE:
                self.input.delete()
            elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL):
                self.input.update(pyperclip.paste())
            else:
                self.input.add(event.unicode)

    def show(self, screen: pygame.Surface):
        super().show(screen)
        self.input.show(screen)


# class TextCard(Card):
#     def __init__(self, text, size, font, font_size, pos, padding=20):
#         super().__init__(size, pos, padding)
#
#         self.font = pygame.font.Font(f"fonts/{font}", font_size)
#         self.text = text
#
#         def show_text(self, screen):
#             max_width = self.rect.right - self.padding - 2
#             x, y = self.rect.left + self.padding, self.rect.centery
#
#             for word in self.text:
#                 word_surface = self.font.render(word, True, (0, 0, 0))
#                 word_width, word_height = word_surface.get_size()
#                 if x + word_width >= max_width:
#                     screen.blit(self.font.render('...', True, (0, 0, 0)), (x, y - word_height / 2))
#                     break
#
#                 screen.blit(word_surface, (x, y - word_height / 2))
#                 x += word_width

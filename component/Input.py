import pygame

from component.Text import Text
from component.Button import Button


class Input:
    def __init__(self, font, length, size, pos, color=(0, 0, 0)):
        self.font = font
        self.word = ""
        self.length = length
        self.text = Text(self.font, self.word[-self.length:], size, pos, color, pos_type='midleft')
        self.size = size
        self.color = color

        self.state = False

        self.fps = 450
        self.fps_counter = pygame.USEREVENT + 3
        self.typing = Button('typing', (8, 25), pos)

    def animation(self):
        if self.state:
            self.typing.state = not self.typing.state

    def add(self, new_char):
        self.word += new_char
        self.update_text()

    def delete(self):
        self.word = self.word[:-1]
        self.update_text()

    def update(self, new_word: str):
        self.word = new_word
        self.update_text()

    def update_text(self):
        text = self.word if len(self.word) <= self.length else self.word[-self.length:]
        self.text = Text(self.font, text, self.size, self.text.rect.midleft, self.color, pos_type='midleft')

    def reset(self):
        self.word = ""
        self.update_text()
        self.state = False

    def show(self, screen):
        self.text.show(screen)
        self.typing.rect = self.typing.img.get_rect(midleft=self.text.rect.midright)
        if self.state and self.typing.state:
            self.typing.show(screen)


class SearchInput(Input):
    def __init__(self, func, size, pos, word_x, font_size=20, length=30):
        super().__init__("字体管家方萌.TTF", length, font_size, (word_x, pos[1]))
        self.img = pygame.image.load(f"images/function/icon_{func}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(center=pos)

    def reset(self):
        super().reset()
        self.state = True

    def show(self, screen):
        super().show(screen)
        screen.blit(self.img, self.rect)


class CardInput(Input):
    def __init__(self, font, pos, word_x, font_size=20, length=20):
        self.word_x = word_x
        super().__init__(font, length, font_size, (pos[0] + word_x, pos[1]))

    def enter(self):
        text = self.word if len(self.word) <= self.length else self.word[0:self.length] + '...'
        self.text = Text(self.font, text, self.size, self.text.rect.midleft, self.color,
                         pos_type='midleft')

    def show(self, screen):
        super().show(screen)

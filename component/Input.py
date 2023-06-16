import pygame

from component.Text import Text
from component.Button import Button


class Input:
    def __init__(self, length, size, pos, color=(0, 0, 0)):
        self.pos = pos
        self.font = "字体管家方萌.TTF"
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
        if self.typing.state:
            self.typing.show(screen)


class CardInput(Input):
    def __init__(self, func, size, pos, word_x, font_size=20, length=30):
        super().__init__(length, font_size, (word_x, pos[1]))
        self.img = pygame.image.load(f"images/function/icon_{func}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(center=pos)

    def reset(self):
        super().reset()
        self.state = True

    def show(self, screen):
        super().show(screen)
        screen.blit(self.img, self.rect)

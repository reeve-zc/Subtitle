import pygame

from setting import *
from component.Button import Button
from component.Card import Card
from component.Text import Text


class CardView:
    def __init__(self, pos, size, space, card_nums, padding):
        self.padding = padding
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.list: list[Card] = []
        self.space = space
        self.nums = card_nums
        self.card_size = size[0] - padding * 2, (size[1] - padding * 2 + space) // card_nums - space
        self.index = 0

    def add_card(self, text):
        self.list.append(Card(text, self.card_size, self.card_size[1] // 4, (0, 0)))

    def get_selected_card(self):
        for index in range(len(self.list)):
            if self.list[index].select:
                return index
            return None

    def delete_card(self, index):
        del self.list[index]

    def show(self, screen: pygame.Surface):
        pygame.draw.line(screen, DEFAULT_COLOR, (self.rect.left, self.rect.top + self.padding), self.rect.bottomleft,
                         width=4)
        # pygame.draw.rect(screen, DEFAULT_COLOR, self.rect, width=4, border_radius=15)


class TodoCardView(CardView):
    def __init__(self):
        super().__init__((90, 210), (350, 460), 10, 5, 30)
        self._title = Text("字体管家方萌.TTF", "TODO", 35, (self.rect.left - 4, self.rect.top - 15), pos_type='midleft',
                           color=DEFAULT_COLOR)

        self._btn_edit = Button('edit', (70, 70), (self.rect.right - 120, self.rect.top - 13))
        self._btn_add = Button('add', (59, 59), (self.rect.right - 75, self.rect.top - 13))
        self._btn_delete = Button('delete', (60, 60), (self.rect.right - 30, self.rect.top - 13))

    def todo_list_pressed(self, pos):
        self._btn_edit.pressed(pos)
        self._btn_add.pressed(pos)
        self._btn_delete.pressed(pos)

    def todo_list_compressed(self):
        pass

    def _add_btn_compressed(self):
        pass

    def show(self, screen: pygame.Surface):
        super().show(screen)
        self._title.show(screen)
        self._btn_delete.show(screen)
        self._btn_add.show(screen)
        self._btn_edit.show(screen)

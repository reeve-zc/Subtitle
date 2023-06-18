import os

import pygame

from setting import *
from component.Button import Button
from component.Card import Card, TodoCard
from component.Text import Text


class CardView:
    def __init__(self, pos, size, space, card_nums, padding):
        self.padding = padding
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.cards = []
        self.space = space
        self.nums = card_nums
        self.card_size = size[0] - padding * 2, (size[1] - padding - (card_nums - 1) * space) // card_nums
        self.top_index = 0

    def get_selected_card(self):
        for index in range(self.top_index, min(self.top_index + self.nums, len(self.cards))):
            if self.cards[index].select:
                return index
        return None

    def delete_card(self, index):
        del self.cards[index]
        if self.top_index > 0:
            self.top_index -= 1

    def set_card_pos(self):
        for i in range(self.top_index, min(self.top_index + self.nums, len(self.cards))):
            card = self.cards[i]
            card.set_pos(
                (self.rect.left + self.padding,
                 self.rect.top + self.padding + (i - self.top_index) * (self.card_size[1] + self.space)))

    def show(self, screen):
        self.set_card_pos()
        cards = self.cards[self.top_index: min(self.top_index + self.nums, len(self.cards))]
        for card in cards:
            card.show(screen)


class TodoCardView(CardView):
    def __init__(self):
        super().__init__((90, 210), (350, 460), 15, 5, 30)
        self._title = Text("字体管家方萌.TTF", "TODO", 35, (self.rect.left - 4, self.rect.top - 15), pos_type='midleft',
                           color=DEFAULT_COLOR)
        self._btn_edit = Button('edit', (70, 70), (self.rect.right - 120, self.rect.top - 13))
        self._btn_add = Button('add', (59, 59), (self.rect.right - 75, self.rect.top - 13))
        self._btn_delete = Button('delete', (60, 60), (self.rect.right - 30, self.rect.top - 13))

        self._active = True

        self.fps = 450
        self.fps_counter = pygame.USEREVENT + 3

        self.cards_initial()

    def cards_initial(self):
        path = "storage/cards.txt"
        if os.path.isfile(path):
            with open(path, 'r') as f:
                texts = f.read().split(",")
                if texts == ['']:
                    return
                for index in range(len(texts)):
                    self.add_card()
                    print("hello")
                    self.cards[index].input.word = texts[index]

    def animation(self):
        index = self.get_selected_card()
        if index is not None:
            self.cards[index].input.animation()

    def add_card(self):
        self.cards.append(TodoCard(self.card_size, (0, 0), self.card_size[1] // 3))
        if len(self.cards) > self.nums:
            self.top_index += 1

    def store_cards(self):
        texts = ""
        for card in self.cards:
            texts += card.get_text() + ','
        with open('storage/cards.txt', 'w') as f:
            f.write(texts[:-1])

    def pressed(self, pos):
        if self._active:
            self._btn_edit.pressed(pos)
            self._btn_add.pressed(pos)
            self._btn_delete.pressed(pos)

            if self._btn_edit.state or self._btn_delete.state:
                return

            cards = self.cards[self.top_index: min(self.top_index + self.nums, len(self.cards))]
            for card in cards:
                card.pressed(pos)

    def compressed(self):
        self._add_btn_compressed()
        self._edit_btn_compressed()
        self._delete_btn_compressed()

        cards = self.cards[self.top_index: min(self.top_index + self.nums, len(self.cards))]
        for card in cards:
            card.compressed()

    def _add_btn_compressed(self):
        if self._btn_add.state:
            self._btn_add.state = False
            self.add_card()

    def _edit_btn_compressed(self):
        if self._btn_edit.state:
            self._btn_edit.state = False
            index = self.get_selected_card()
            if index is not None:
                self.cards[index].input.state = True
                self.cards[index].input.update_text()

    def _delete_btn_compressed(self):
        if self._btn_delete.state:
            self._btn_delete.state = False
            index = self.get_selected_card()
            if index is not None:
                self.delete_card(index)

    def todo_list_key_down(self, event):
        cards = self.cards[self.top_index: min(self.top_index + self.nums, len(self.cards))]
        for card in cards:
            card.card_key_down(event)

    def show(self, screen: pygame.Surface):
        super().show(screen)
        pygame.draw.line(screen, DEFAULT_COLOR, (self.rect.left, self.rect.top + self.padding), self.rect.bottomleft,
                         width=4)
        self._title.show(screen)
        self._btn_delete.show(screen)
        self._btn_add.show(screen)
        self._btn_edit.show(screen)

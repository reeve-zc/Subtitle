import os
import shutil
import pygame
import pyperclip

from component.Button import Button
from component.Input import SearchInput
from component.Text import Text
from component.FloatingInterface import FloatingInterface
from setting import *
from utils.get_audio import get_info, download_song


class Search:
    def __init__(self):
        self._btn_search = Button("search", (90, 90), (270, 120))
        self._btn_mp3_download = Button("button", (635, 95), (WIDTH / 2 + 3, 520))
        self._input = SearchInput('searchbar', (SEARCH_BAR_WIDTH, SEARCH_BAR_HEIGHT), SEARCH_BAR_CENTER, 420, length=40)
        self._floating_interface = FloatingInterface((SEARCH_SURFACE_WIDTH, SEARCH_SURFACE_HEIGHT))

        self._font = {18: pygame.font.Font("fonts/字体管家方萌.TTF", 18),
                      20: pygame.font.Font("fonts/字体管家方萌.TTF", 20),
                      24: pygame.font.Font("fonts/字体管家方萌.TTF", 24)}
        self._result = None
        self._state = False
        self._active = True

    def show_download_btn(self, screen: pygame.Surface):
        self._btn_mp3_download.show(screen)
        word = self._font[20].render('Download mp3', True, (0, 0, 0))
        x = self._btn_mp3_download.rect.centerx - word.get_width() / 2
        y = self._btn_mp3_download.rect.centery - word.get_height() / 2
        screen.blit(word, (x, y))

    def mp3_download_btn_pressed(self, pos):
        if self._result and self._btn_mp3_download.rect.collidepoint(pos):
            self._btn_mp3_download.state = True

    def mp3_download_btn_compressed(self):
        if self._btn_mp3_download.state:
            self._btn_mp3_download.state = False
            result = download_song(self._input.word)
            if result:
                self._result = result

    def search_bar_pressed(self, pos):
        if self._input.rect.collidepoint(pos):
            self._input.state = True
        else:
            self._input.state = False

    def search_bar_key_down(self, event: pygame.event):
        if self._input.state:
            if event.key == pygame.K_RETURN:
                if os.path.isdir("temp/"):
                    shutil.rmtree("temp/")
                self._result = get_info(self._input.word)
            elif event.key == pygame.K_BACKSPACE:
                self._input.delete()
            elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL):
                self._input.update(pyperclip.paste())
            else:
                self._input.add(event.unicode)

    def pressed(self, pos):
        if self._active:
            self._btn_search.pressed(pos)
            self._floating_interface.btn_close.pressed(pos)
            self.search_bar_pressed(pos)
            self.mp3_download_btn_pressed(pos)

    def compressed(self):
        self.mp3_download_btn_compressed()
        self.search_btn_compressed()
        self.close_btn_compressed()
        return self._state

    def search_btn_compressed(self):
        if self._btn_search.state:
            self._btn_search.state = False
            self._state = True
            self._input.reset()

    def close_btn_compressed(self):
        if self._floating_interface.btn_close.state:
            self._floating_interface.btn_close.state = False
            self._result = None
            self._state = False

            if os.path.isdir("temp/"):
                shutil.rmtree("temp/")

    def show_result(self, screen):
        if self._result and self._result == "Download Failed":
            text = Text("字体管家方萌.TTF", "Not Found", 45, CENTER)
            text.show(screen)
        elif self._result:
            img_name = list(filter(lambda x: 'jpg' in x, os.listdir("temp/")))[0]
            img = pygame.image.load("temp/" + img_name).convert()
            img = pygame.transform.scale(img, (280, 160))
            screen.blit(img, (350, 310))

            max_width, max_height = 900, 390
            x, y = 645, 310
            for word in self._result[0]:
                word_surface = self._font[24].render(word, True, (0, 0, 0))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    if y + word_height >= max_height:
                        screen.blit(self._font[24].render('...', True, (0, 0, 0)), (x, y))
                        break
                    x = 645  # Reset the x.
                    y += word_height  # Start on new row.

                screen.blit(word_surface, (x, y))
                x += word_width

            pygame.draw.line(screen, (0, 0, 0), (645, 400), (910, 400), width=3)

            screen.blit(self._font[18].render("Time: " + self._result[1], True, (0, 0, 0)), (645, 415))

            x, y = 645, 440
            for word in self._result[2]:
                word_surface = self._font[18].render(word, True, (0, 0, 0))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    screen.blit(self._font[18].render('...', True, (0, 0, 0)), (x, y))
                    break

                screen.blit(word_surface, (x, y))
                x += word_width

        else:
            text = Text("字体管家方萌.TTF", "Not Found", 45, CENTER)
            text.show(screen)

    def show(self, screen: pygame.Surface):
        if self._state:
            self._floating_interface.show(screen)
            self._input.show(screen)
            self.show_result(screen)

            if self._result:
                self.show_download_btn(screen)

    @property
    def input(self):
        return self._input

    @property
    def btn_search(self):
        return self._btn_search

import pygame.draw
import pygame.font

from component.Button import Button
from setting import *
from utils.common import clamp, time_trans_m


class Bar:
    def __init__(self, x, y, length, scale):
        self._x, self._y, self._length = x, y, length
        self._rect = pygame.Rect(x - BAR_CIRCLE_RADIUS, y - BAR_CIRCLE_RADIUS, BAR_CIRCLE_SIZE, BAR_CIRCLE_SIZE)
        self._line_rect = pygame.Rect(x - BAR_CIRCLE_RADIUS, y - BAR_CIRCLE_RADIUS - 10, length + BAR_CIRCLE_SIZE,
                                      BAR_CIRCLE_SIZE + 20)

        self._scale = scale
        self._state = False

    def get_pos(self):
        delta_x = self._rect.centerx - self._x
        return delta_x / (self._length / self._scale)

    def set_pos(self, pos):
        mx = clamp(self._x, self._x + self._length, pos[0])
        self._rect.centerx = mx

    def show(self, screen: pygame.Surface):
        cx, cy = self._rect.center
        if self._state:
            self._rect.size = BAR_CIRCLE_SIZE + 2, BAR_CIRCLE_SIZE + 2
        else:
            self._rect.size = BAR_CIRCLE_SIZE, BAR_CIRCLE_SIZE

        self._rect.center = cx, cy
        pygame.draw.line(screen, DEFAULT_COLOR, (self._x, self._y), (self._x + self._length, self._y), width=LINE_WIDTH)
        pygame.draw.line(screen, DEFAULT_COLOR_GRAY, (cx, self._y), (self._x + self._length, self._y), width=LINE_WIDTH)
        pygame.draw.rect(screen, DEFAULT_COLOR, self._rect, border_radius=int(self._rect.h / 2))


class SoundBar(Bar):
    def __init__(self):
        super().__init__(SOUND_BAR_X_START, SOUND_BAR_Y, SOUND_BAR_LENGTH, 100)
        self._rect.centerx += self._length / 2

        self._btn_volume = Button("volume", (50, 50), (self._x - 26, self._y))
        self._btn_mute = Button("mute", (50, 50), (self._x - 26, self._y))
        self._last = 0
        self._mute = False

    def set_pos(self, pos):
        super().set_pos(pos)
        self._mute = True if self._rect.centerx == self._x else False

    def reverse_state(self):
        self._mute = not self._mute
        if self._mute:
            self._last = self._rect.centerx
            self._rect.centerx = SOUND_BAR_X_START
        else:
            self._rect.centerx = self._last

    def show(self, screen: pygame.Surface):
        super().show(screen)

        if self._mute:
            self._btn_mute.show(screen)
        else:
            self._btn_volume.show(screen)

    @property
    def rect(self):
        return self._rect

    @property
    def line_rect(self):
        return self._line_rect

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def btn_volume(self):
        return self._btn_volume


class PlayBackBar(Bar):
    def __init__(self):
        super().__init__(X_START, PLAYBACK_BAR_Y, LENGTH, 0)
        self.font = pygame.font.Font("fonts/Arial.ttf", 19)

    def reset(self):
        super().__init__(X_START, PLAYBACK_BAR_Y, LENGTH, 0)

    def moving(self, time):
        delta_x = time * (self._length / self._scale)
        self._rect.centerx = self._x + delta_x

    def set_pos(self, pos):
        super().set_pos(pos)
        return self.get_pos()

    def _show_time(self):
        now = time_trans_m(int(self.get_pos()))
        duration = time_trans_m(int(self._scale))
        time = self.font.render(f"{now} / {duration}", True, DEFAULT_COLOR)
        surface = pygame.Surface((time.get_width(), time.get_height()), flags=pygame.HWSURFACE).convert_alpha()
        surface.fill((255, 255, 255, 0))
        surface.blit(time, (0, 0))
        return surface

    def show(self, screen: pygame.Surface):
        super().show(screen)

        pygame.draw.line(screen, DEFAULT_COLOR, (self._x, self._y), (self._rect.centerx, self._y), width=LINE_WIDTH + 2)
        pygame.draw.rect(screen, DEFAULT_COLOR, self._rect, border_radius=int(self._rect.h / 2))
        screen.blit(self._show_time(), (self._x, Y_START + PLAYBACK_BAR_MARGIN_TOP / 2 - 11))

    @property
    def rect(self):
        return self._rect

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def duration(self):
        return self._scale

    @duration.setter
    def duration(self, value):
        self._scale = value

    @property
    def line_rect(self):
        return self._line_rect


class ScrollBar:
    def __init__(self, x, y, width, length, scale, item_amount, color):
        self._x, self._y, self._length = x, y, length
        rect_length = item_amount / scale * length
        self._rect = pygame.Rect(x - width / 2 + 4, y, width, rect_length)
        self._color = color

        self._last = (0, 0)
        self._scale = scale
        self._state = False

    def get_pos(self):
        delta_x = self._rect.centerx - self._x
        return delta_x / (self._length / self._scale)

    def set_pos(self, pos):
        mx = clamp(self._x, self._x + self._length, pos[0])
        self._rect.centerx = mx

    def show(self, screen: pygame.Surface):
        pygame.draw.line(screen, self._color, (self._x, self._y), (self._x, self._y + self._length), width=8)
        pygame.draw.rect(screen, self._color, self._rect, border_radius=6)

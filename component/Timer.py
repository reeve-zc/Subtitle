import pygame
from setting import *
from component.Text import Text


class Timer:
    def __init__(self):
        self.current_time = WORKING_LENGTH
        self.color = DEFAULT_COLOR_GRAY

        self.timer_text = Text('字体管家方萌.TTF', '25:00', 120, (710, 180), self.color)
        self.mode_working = Text('字体管家方萌.TTF', 'laboring', 30, (625, 80), DEFAULT_COLOR)
        self.mode_short_break = Text('字体管家方萌.TTF', 'short rest', 30, (825, 80), DEFAULT_COLOR_PINK)
        self.mode_long_break = Text('字体管家方萌.TTF', 'long rest', 30, (1025, 80), DEFAULT_COLOR_BLUE)

        self.counting = False
        self.end = False
        self.state = False
        self.zero_state = False

        self.mode = 0
        self.round = [0, 0, 0]

        self.work_count = Text('字体管家方萌.TTF', f"{self.round[0]}", 40, (180, 698), DEFAULT_COLOR)
        self.short_break_count = Text('字体管家方萌.TTF', f"{self.round[1]}", 40, (285, 698), DEFAULT_COLOR_PINK)
        self.long_break_count = Text('字体管家方萌.TTF', f"{self.round[2]}", 40, (390, 698), DEFAULT_COLOR_BLUE)

        self.fps = 1000
        self.fps_counter = pygame.USEREVENT + 2

    def animation(self):
        self.current_time = self.current_time - 1 if self.current_time >= 0 else 0

    def update_time(self, time):
        self.current_time = time

    def get_time_text(self):
        if self.current_time == 0:
            if self.zero_state:
                self.round[self.mode] += 1
                self.work_count.update(str(self.round[0]))
                self.short_break_count.update(str(self.round[1]))
                self.long_break_count.update(str(self.round[2]))
                self.zero_state = False
            self.counting = False
            self.end = True
            return "00:00"
        else:
            self.zero_state = True
            return f"{self.current_time // 60:02}:{self.current_time % 60:02}"

    def get_color(self):
        if not self.counting:
            return DEFAULT_COLOR_GRAY
        return TIMER_COLOR[self.mode]

    def show(self, screen: pygame.Surface):
        self.mode_working.show(screen)
        self.mode_short_break.show(screen)
        self.mode_long_break.show(screen)
        self.work_count.show(screen)
        self.short_break_count.show(screen)
        self.long_break_count.show(screen)

        self.timer_text.update(self.get_time_text(), self.get_color())
        self.timer_text.show(screen)

    def pressed(self, pos):  # 被按下的瞬間的設定_動作集合
        self._current_time_pressed(pos)
        self._mode_select_pressed(pos)

    def compressed(self):  # 按下放開瞬間的讀取_動作集合
        self._count_compressed()

    def _current_time_pressed(self, pos):
        if self.timer_text.rect.collidepoint(pos):
            self.state = True
        else:
            self.state = False

    def _count_compressed(self):
        if self.state:
            if self.end:
                self.current_time = WORKING_LENGTH
                self.end = False
            self.counting = not self.counting

    def _mode_select_pressed(self, pos):
        if self.mode_working.rect.collidepoint(pos):  # normal
            self.state = True
            self.mode = 0
            self.current_time = TIME_LENGTH[self.mode]

        elif self.mode_short_break.rect.collidepoint(pos):  # short break
            self.state = True
            self.mode = 1
            self.current_time = TIME_LENGTH[self.mode]

        elif self.mode_long_break.rect.collidepoint(pos):  # long break
            self.state = True
            self.mode = 2
            self.current_time = TIME_LENGTH[self.mode]

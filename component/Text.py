import pygame


class Text:
    def __init__(self, font, text, size, pos, color=(0, 0, 0), pos_type='center'):
        self._font = pygame.font.Font(f"fonts/{font}", size)
        self._color = color
        self._text = self._font.render(text, True, color)
        self._pos_type = pos_type
        self._state = False
        if pos_type == 'center':
            self.rect = self._text.get_rect(center=pos)
        elif pos_type == 'midleft':
            self.rect = self._text.get_rect(midleft=pos)

    def update(self, text, color=None):
        if color:
            self._color = color
        self._text = self._font.render(text, True, self._color)
        if self._pos_type == 'center':
            self.rect = self._text.get_rect(center=self.rect.center)
        elif self._pos_type == 'midleft':
            self.rect = self._text.get_rect(midleft=self.rect.midleft)

    def show(self, screen: pygame.Surface):
        screen.blit(self._text, self.rect)

    @property
    def state(self):
        return self._state

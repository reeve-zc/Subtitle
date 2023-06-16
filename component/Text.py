import pygame


class Text:
    def __init__(self, font, text, size, pos, color=(0, 0, 0), pos_type='center'):
        font = pygame.font.Font(f"fonts/{font}", size)
        self._color = color
        self._text = font.render(text, True, color)
        self._pos_type = pos_type
        if pos_type == 'center':
            self.rect = self._text.get_rect(center=pos)
        elif pos_type == 'midleft':
            self.rect = self._text.get_rect(midleft=pos)

    def show(self, screen: pygame.Surface):
        screen.blit(self._text, self.rect)

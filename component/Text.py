import pygame


class Text:
    def __init__(self, text, size, pos, color=(0, 0, 0), pos_type='center'):
        font = pygame.font.Font("fonts/字体管家方萌.TTF", size)
        self.text = font.render(text, True, color)
        if pos_type == 'center':
            self.rect = self.text.get_rect(center=pos)
        elif pos_type == 'midleft':
            self.rect = self.text.get_rect(midleft=pos)

    def show(self, screen: pygame.Surface):
        screen.blit(self.text, self.rect)

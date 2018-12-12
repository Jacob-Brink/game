import pygame
from lib.modules.gui.rectangle import Point

class Text:

    def __init__(self, text, font_size, color, pos, y_value):
        '''
        Class models text and makes creating text in the game more intuitive
        '''        
        self._text = text
        self._font_size = font_size
        self._color = color
        self._pos = pos
        self._y_value = y_value

        self._font = pygame.font.SysFont(None, self._font_size)
        self._surface = self._font.render(self._text, 1, color)
        self._text_size = self._font.size(self._text)
        self._text_width = self._text_size[0]
        
    def get_rect(self, screen_width):
        '''Return pygame.Rect for Textbox'''
        return pygame.Rect((0 if self._pos == 'left' else screen_width/2 - self._text_width/2 if self._pos == 'middle' else screen_width-self._text_width, self._y_value), self._text_size)

    
    def get_surface(self):
        '''Return surface'''
        return self._surface

    def change_pos(self, pos):
        '''Change position'''
        self._pos = pos
    
    def get_surface_and_pos(self, screen_width):
        '''Allows each view to send surface to view renderer'''
        return (self._surface, Point(self.get_rect(screen_width).x, self.get_rect(screen_width).y))

def init():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()

    return screen


if __name__ == '__main__':

    screen = init()

    for i in range(0, 1000):

        screen.fill((0,0,0))

        t = Text(str(i), i // 10, (255,0,100), (20, 20), screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                break

        t.render()
        pygame.display.flip()

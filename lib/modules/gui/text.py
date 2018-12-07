import pygame

class Text:

    def __init__(self, text, size, color, pos):
        '''
        Class models text and makes creating text in the game more intuitive
        '''

        self._text = text
        self._size = size
        self._color = color
        self._pos = pos

        self._font = pygame.font.SysFont(None, self._size)
        self._surface = self._font.render(self._text, 1, color)

    def get_rect(self):
        '''Return pygame.Rect for Textbox'''
        return pygame.Rect(self._pos, self._font.size(self._text))

    def get_surface(self):
        '''Return surface'''
        return self._surface

    def get_surface_and_pos(self):
        '''Allows each view to send surface to view renderer'''
        return [self._surface, self._pos]



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

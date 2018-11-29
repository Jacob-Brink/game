import pygame

class Image:

    def __init__(self, image_file_path, screen, pos):
        '''
        Constructor models an image, making displaying images easy and intuitive
        '''

        self._pos = pos
        self._path = image_file_path
        self._screen = screen
        self._surface = pygame.image.load(self._path)

    def render(self):
        '''
        Render Image to screen provided in constructor
        '''

        self._screen.blit(self._surface, self._pos)

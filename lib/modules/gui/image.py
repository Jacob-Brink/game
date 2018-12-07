import pygame

class Image:

    def __init__(self, image_file_path):
        '''
        Constructor models an image, making displaying images easy and intuitive
        '''

        self._path = image_file_path
        self._surface = pygame.image.load(self._path)

    def return_surface(self):
        '''Returns only the surface'''
        return self._surface

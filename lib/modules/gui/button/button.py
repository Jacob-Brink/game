import pygame
from pygame import Rect

class Button:

    def __init__(self, text, callback, color_tuple, screen, font_size, coordinate_tuple):


        self._coordinate_tuple = coordinate_tuple
        self._text = text
        self._font = pygame.font.SysFont(None, font_size)
        self._rect = Rect(self._coordinate_tuple, self._font.size(text))

        self._callback = callback
        
        self._hover_surface = self._font.render(self._text, 1, (0, 255, 0))
        self._normal_surface = self._font.render(self._text, 1, (0, 0, 255))
        self._text_surface = self._normal_surface

        self._screen = screen
        
    def _hover(self):
        
        self._text_surface = self._hover_surface

    def _draw_button(self):

        self._screen.blit(self._text_surface, self._coordinate_tuple)
        
    def update(self, mouse_pos, event):

        #if mouse hovers over button
        if self._rect.collidepoint(mouse_pos):

            self._hover()
            
            #if mouse is clicked call callback
            if event:

                self._callback()

            #if no mouse click call hover
            else:

                self._hover()

        #if mouse does not hover over button
        else:

            self._text_surface = self._normal_surface


        self._draw_button()

import pygame

class Button:

    def __init__(self, text, callback, screen, font_size, coordinate_tuple):
        '''
        Constructs a button with the text, creates surface constants: one for when the mouse hovers
        over the button, and one for when the mouse does not hover over the button.
        '''

        self._coordinate_tuple = coordinate_tuple
        self._text = text
        self._font = pygame.font.SysFont(None, font_size)
        self._rect = pygame.Rect(self._coordinate_tuple, self._font.size(text))

        self._callback = callback

        self._HOVER_SURFACE = self._font.render(self._text, 1, (24, 100, 240))
        self._NORMAL_SURFACE = self._font.render(self._text, 1, (0, 0, 255))
        self._text_surface = self._NORMAL_SURFACE

        self._screen = screen
        

    def _draw_button(self):
        '''
        Private function which draws the button.
        '''
    
        self._screen.blit(self._text_surface, self._coordinate_tuple)

        
    def update(self, mouse_pos, event):
        '''
        Update function updates the Button with mouse events. If the mouse hovers, the displayed text 
        surface is assigned the hover surface. If not, the displayed text will be the normal surface
        '''
        
        #if mouse hovers over button
        if self._rect.collidepoint(mouse_pos):

            self._text_surface = self._HOVER_SURFACE
            
            #if mouse is clicked call callback
            if event:

                self._callback()

        #if mouse does not hover over button
        else:

            self._text_surface = self._NORMAL_SURFACE


        self._draw_button()

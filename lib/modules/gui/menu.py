from button import Button

import pygame

#acceptable values for position argument
acceptable_positions = ['left', 'right', 'middle']

class Menu:

    def __init__(self, screen, position):

        #checks if position parameter holds appropriate value
        if (not isinstance(position, str)) and (position not in acceptable_positions):

            raise ValueError('Menu->Constructor: position parameter must be of type str')
        
        self._position = position
        self._font_size = 32
        self._buttons = []
        self._screen = screen
        self._margin = 10
        
    def add_button(self, text, callback):

        y = len(self._buttons)*self._font_size
        text_length = pygame.font.SysFont(None, self._font_size).size(text)[0]
        screen_width = self._screen.get_width()

        
        if self._position == 'left':
            x = self._margin
    
        elif self._position == 'middle':
            x = (screen_width // 2) - (text_length // 2)
            
        elif self._position == 'right':
            x = screen_width - (self._margin + text_length)
            
            
        self._buttons.append(Button(text, callback, (0, 255, 255), self._screen, self._font_size, (x,y)))
        
    def update(self, mouse_event, click):

        for button in self._buttons:

            button.update(mouse_event, click)

            

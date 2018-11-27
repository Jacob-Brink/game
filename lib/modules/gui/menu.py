#If program is run as main, button cannot be imported with path relative to main.py
if __name__ == '__main__':
    from button import Button
    from view import View
#If program is run as module, button must be imported relative to main.py
else:
    from lib.modules.gui.view import View
    from lib.modules.gui.button import Button

import pygame

#acceptable values for position argument
acceptable_positions = ['left', 'right', 'middle']

class Menu(View):

    def __init__(self, screen, position, title, ID):
        '''
        Constructor constructs Menu object, which will setup the font, title, and all variables required for a menu with buttons
        '''

        View.__init__(self, ID)
        
        #checks if position parameter holds appropriate value
        if (not isinstance(position, str)) or (position not in acceptable_positions):

            raise ValueError('Menu->Constructor: position parameter must be one of following strings: left, right, or middle')
        
        #checks if title is a string
        if not isinstance(title, str):

            raise ValueError('Menu->Constructor: title parameter must be of type str')
        
        #title surface creation
        self._title = title
        self._font = pygame.font.SysFont(None, 32)
        self._title_surface = self._font.render(self._title, 1, (0, 255, 0))

        #button setup
        self._position = position
        self._font_size = 32
        self._buttons = []
        self._screen = screen
        self._margin = 10

    def click_callback(self, ID):
        self.view_switch(ID)
        
        
    #adds a button with text and a callback
    def add_button(self, text, ID):
        '''
        Adds a button to the button list on the menu. Takes Text and a callback to be called on when button is clicked
        '''
        
        screen_width = self._screen.get_width()
        screen_height = self._screen.get_height()

        y = len(self._buttons)*self._font_size + screen_height / 8
        text_length = pygame.font.SysFont(None, self._font_size).size(text)[0]
        
        if self._position == 'left':
            x = self._margin
    
        elif self._position == 'middle':
            x = (screen_width // 2) - (text_length // 2)
            
        elif self._position == 'right':
            x = screen_width - (self._margin + text_length)
            

        
        self._buttons.append(Button(text, callback, (0, 255, 255), self._screen, self._font_size, (x,y)))
        
    def update(self, mouse_event, click):
        '''
        Will update the menu with realtime events, such as the mouse events. It also updates the buttons in the menu
        '''
        
        self._screen.blit(self._title_surface, (0,0))
        
        for button in self._buttons:

            button.update(mouse_event, click)






            
            
if __name__ == '__main__':
    '''
    Following code tests menu code for its constructor value errors
    '''

    
    #test wrong position value
    try:

        menu = Menu(1, 'bad value for position', 'title')

    except ValueError as e:

        assert str(e) == 'Menu->Constructor: position parameter must be one of following strings: left, right, or middle'

    #test wrong position type
    try:

        menu = Menu(1, 3141, 'title')
           
    except ValueError as e:

        assert str(e) == 'Menu->Constructor: position parameter must be one of following strings: left, right, or middle'

    #test wrong title type
    try:
        menu = Menu(1, 'left', 123)
        
    except ValueError as e:
        
        assert str(e) == 'Menu->Constructor: title parameter must be of type str'
        
    print('\nAll Tests Passed.')

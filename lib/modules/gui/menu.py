# If program is run as main, button cannot be imported with path relative to main.py
if __name__ == '__main__':
    from button import Button
    from view import View
# If program is run as module, button must be imported relative to main.py
else:
    from lib.modules.gui.view import View
    from lib.modules.gui.button import Button

import pygame

# acceptable values for position argument
acceptable_positions = ['left', 'right', 'middle']




class Menu(View):

    def __init__(self, screen, position, title):
        '''
        Constructor constructs Menu object, which will setup the font, title, and all variables required for a menu with buttons
        '''

        super().__init__(ID)
        
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

    def click(self, ID):
        '''
        Button click callback.
        '''
        super().switch(ID)

        
    def click_callback(self, ID):
        '''
        Wrapper for click_callback
        When a button is clicked, it will call this callback with a unique id matching another view or task.
        '''
        
        def return_func():
            
            self.click(ID)

        return return_func
        
    
    # adds a button with text and a callback
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
            

        self._buttons.append(Button(text, self.click_callback(ID), self._screen, self._font_size, (x,y)))
        
    def update(self, event):
        '''
        Will update the menu with realtime events, such as the mouse events. It also updates the buttons in the menu
        '''
        
        self._screen.blit(self._title_surface, (0,0))
        
        for button in self._buttons:

            button.update(event)





def init():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()
    
    return screen



            
            
if __name__ == '__main__':
    '''
    Following code tests menu code for its constructor value errors, button creation, button click, and button callback.
    '''

    import pygame

    screen = init()
    

    
    # test wrong position value
    try:

        menu = Menu(screen, 'bad value for position', 'title', 1)

    except ValueError as e:

        assert str(e) == 'Menu->Constructor: position parameter must be one of following strings: left, right, or middle'

        
    # test wrong position type
    try:

        menu = Menu(screen, 3141, 'title', 1)
           
    except ValueError as e:

        assert str(e) == 'Menu->Constructor: position parameter must be one of following strings: left, right, or middle'

        
    # test wrong title type
    try:
        menu = Menu(screen, 'left', 123, 1)
        
    except ValueError as e:
        
        assert str(e) == 'Menu->Constructor: title parameter must be of type str'

        
    # test mouse position on button with click set to True
    # test callback and view handling
    try:

        mouse_position = (20, 60)

        menu = Menu(screen, 'left', 'title', 2)

        # next view id should be 0 when no button has been pressed
        assert menu.get_new_view() == 0


        menu.add_button('this button is clicked', 3)
        menu.add_button('this button is not clicked', 4)

        # update buttons each with a click
        menu.update(mouse_position, True)

        # button with id 3 is clicked and should trigger parent class View next_view_id
        assert menu.get_new_view() == 3
        
    except:
        
        assert False
    
        
    print('\nAll Tests Passed.')

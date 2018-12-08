# If program is run as main, button cannot be imported with path relative to main.py
if __name__ == '__main__':
    from button import Button
    from view import View
# If program is run as module, button must be imported relative to main.py
else:
    from lib.modules.gui.view import View
    from lib.modules.gui.button import Button
    from lib.modules.gui.text import Text
    from lib.modules.gui.events import *

import pygame

# acceptable values for position argument
acceptable_positions = ['left', 'right', 'middle']

class Menu(View):

    def __init__(self, screen, position, title, *buttons):
        '''Constructor constructs Menu object, which will setup the font, title, and all variables required for a menu with buttons'''

        # Initialize View parent
        super().__init__(screen, pygame.Rect((0,0), screen.get_size()))
        
        #save parameters for sending to next View so it can go back
        self._parameters = screen, position, title, *buttons

        # checks if position parameter holds appropriate value
        if (not isinstance(position, str)) or (position not in acceptable_positions):

            raise ValueError('Menu->Constructor: position parameter must be one of following strings: left, right, or middle')

        #checks if title is a string
        if not isinstance(title, str):

            raise ValueError('Menu->Constructor: title parameter must be of type str')

        #title surface creation
        self._title_text = title
        self._title_surface = Text(self._title_text, 32, (200, 100, 20), (screen.get_width()/2, 20))

        #button setup
        self._position = position
        self._font_size = 32
        self._buttons = []
        self._margin = 10

        for button in buttons:
            self.add_button(button[0], button[1])


    def add_button(self, text, callback):
        '''Adds a button to the button list on the menu. Takes Text and a callback to be called on when button is clicked'''

        screen_width = super().return_screen_dimensions()[0]
        screen_height = super().return_screen_dimensions()[1]

        y = len(self._buttons)*self._font_size + screen_height / 8

        text_length = pygame.font.SysFont(None, self._font_size).size(text)[0]

        if self._position == 'left':
            x = self._margin

        elif self._position == 'middle':
            x = (screen_width // 2) - (text_length // 2)

        elif self._position == 'right':
            x = screen_width - (self._margin + text_length)

        hover_surface = Text(text, 32, (200, 200, 200), (x, y))
        normal_surface = Text(text, 30, (100, 10, 40), (x, y))

        self._buttons.append(Button(normal_surface, hover_surface, callback))


    def update(self, event):
        '''Will update the menu with realtime events, such as the mouse events. It also updates the buttons in the menu'''
        screen = event.screen()
        
        for button in self._buttons:
            button.update(event)
            if button.is_clicked():
                button.return_callback()(Menu, self._parameters)

        super().render(screen, self._title_surface.get_surface_and_pos(), *[button.return_surface().get_surface_and_pos() for button in self._buttons])



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

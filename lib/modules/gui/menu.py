
from lib.modules.gui.view import View
from lib.modules.gui.button import Button
from lib.modules.gui.text import Text
from lib.modules.gui.events import *

from lib.modules.game.bomb import Bomb
from lib.modules.physics.physics_engine import Physics
from lib.modules.physics.vector import Vector

from random import randint
import pygame

# acceptable values for position argument
acceptable_positions = ['left', 'right', 'middle']
BUTTON_COLOR = (255, 155, 100)
HIGHLIGHT_COLOR = (100, 200, 100)
TITLE_COLOR = (12, 100, 200)


class Menu(View):

    def __init__(self, screen, position, title, buttons):
        '''Constructor constructs Menu object, which will setup the font, title, and all variables required for a menu with buttons'''

        # Initialize View parent
        super().__init__(screen)
        
        #save parameters for sending to next View so it can go back
        self._parameters = screen, position, title, buttons

        # checks if position parameter holds appropriate value
        if (not isinstance(position, str)) or (position not in acceptable_positions):

            raise ValueError('Menu->Constructor: position parameter must be one of following strings: left, right, or middle')

        #checks if title is a string
        if not isinstance(title, str):

            raise ValueError('Menu->Constructor: title parameter must be of type str')
        
        #button setup
        self._position = position
        self._font_size = 32
        self._buttons = []
        self._margin = 10

        # for show, have bomb list
        self._physics = Physics(False)
        self._bomb_list = []
        
        for button in buttons:
            self.add_button(button[0], button[1])
        
        #title surface creation
        self._title_text = title
        self._title_surface = Text(self._title_text, 32, TITLE_COLOR, self._position, 20)


    def add_button(self, text, callback):
        '''Adds a button to the button list on the menu. Takes Text and a callback to be called on when button is clicked'''

        screen_width = super().return_screen_dimensions().x()
        screen_height = super().return_screen_dimensions().y()

        y = len(self._buttons)*self._font_size + screen_height / 8

        text_length = pygame.font.SysFont(None, self._font_size).size(text)[0]

        hover_surface = Text(text, 32, HIGHLIGHT_COLOR, self._position, y)
        normal_surface = Text(text, 30, BUTTON_COLOR, self._position, y)

        self._buttons.append(Button(normal_surface, hover_surface, callback))

    def create_bomb(self, position):
        '''Create bomb and append to bomb list'''
        s_dimensions = super().return_screen_dimensions()
        screen_width = s_dimensions.x()
        screen_height = s_dimensions.y()
        
        random_x = position.x()
        random_y = position.y()

        random_magnitude = randint(1,4)/100
        random_direction = randint(-180,180)
        
        self._bomb_list.append(Bomb(Vector(Point(random_x, random_y), magnitude=random_magnitude, direction=random_direction)))

    def update(self, event):
        '''Will update the menu with realtime events, such as the mouse events. It also updates the buttons in the menu'''
        screen = event.screen()

        # update buttons
        for button in self._buttons:
            button.update(event)
            
            if button.is_clicked():
                button.return_callback()(Menu, self._parameters)

        # render buttons
        super().render(self._title_surface.get_surface_and_pos(screen.get_size()[0]), *[button.return_surface().get_surface_and_pos(screen.get_size()[0]) for button in self._buttons])
        
        # update physics with only bombs
        self._physics.update(event, [], self._bomb_list, [])    
        
        # draw bombs
        for bomb in self._bomb_list:
            
            if super().is_visible(bomb.return_rect()):
                super().render_rectangle(bomb.return_rect(), color=bomb.get_color())
            
        # randomly create a bomb by random numbers
        create_bomb = randint(0,4)
       
        if create_bomb == 1:
            self.create_bomb(event.mouse().get_position())

        
        


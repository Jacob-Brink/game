from lib.modules.game.game import Game
from lib.modules.gui.view import View
from lib.modules.gui.text import Text
from lib.modules.gui.events import Switch
from lib.modules.game.timer import Timer

import pygame

# steps including tile for each step and required key presses for each step in the tutorial

COLOR = (255, 0, 0)


class GameTutorial(View):

    def __init__(self, screen, level, go_back):
        '''Constructs Tutorial Class'''
        super().__init__(screen)
        self._screen = screen
        self._game = Game(screen, level, go_back, False)
        self._steps = [{'title': 'Welcome to the Tutorial! To Continue Press the Space Bar', 'required': [pygame.K_SPACE]},
         {'title': 'In the tutorial, you must try out every command key before proceeding to the next stage. Press the Space Bar', 'required': [pygame.K_SPACE]},
         {'title': 'Press w,a,s,d keys or arrow keys to move. Try moving around.', 'required': [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]},
         {'title': 'Jumping in air is possible. Try a double jump with the arrow keys and w key', 'required': [pygame.K_w, pygame.K_w, pygame.K_UP, pygame.K_UP]},
         {'title': 'Press f or right control to shoot explosive bombs. Explosive bombs deal damage, and can act as force field', 'required': [pygame.K_f, pygame.K_RCTRL]},
         {'title': 'Press r or right shift to shoot implosive bombs. Implosive bombs deal no damage, and are disguised as explosive bombs.', 'required': [pygame.K_r, pygame.K_RSHIFT]},
         {'title': 'Congratulations on completing the tutorial! Press escape to exit to the main menu.', 'required': [pygame.K_ESCAPE]} ]

        self._position = 0
        self._limit = len(self._steps)
        self.set_text()
        self._finished = False

        self._timer = Timer()
        self._time_limit = 2
        
    def set_text(self):
        '''Sets current text to message'''
        self._text = Text(self._steps[self._position]['title'], 32, COLOR, 'left', 20)
       
        
    def update(self, events):
        '''Update game tutorial. https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating. From this website I learned how to iterate through a list while popping elements by using list comprehenion'''

        # update game
        self._game.update(events)

        if not self._finished:
        
            # keys pressed
            k_pressed = events.keyboard().is_pressed

            # create new list without keys pressed
            needed_keys = self._steps[self._position]['required']

            self._steps[self._position]['required'] = [key for key in needed_keys if not k_pressed(key) == Switch.pushed_up]

            # when the needed keys list in either player 1 or player 2 keyboard layout are all pressed, go to next part of tutorial
            if len(self._steps[self._position]['required']) == 0 and self._timer.read() == -1:

                self._timer.restart()

            if self._timer.read() > self._time_limit:

                self._position += 1
                self._game.start_game()    
                self.set_text()

                self._timer.stop()

                # when finished set finished to true
                if self._position == self._limit:
                    self._finished = True

        super().render(self._text.get_surface_and_pos(self._screen.get_width()), relative_screen=True)
        
                    
            
        

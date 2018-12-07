import os

from lib.modules.gui.editor import Editor
from lib.modules.gui.menu import Menu
from lib.modules.game.game import Game

class Handler:

    def __init__(self, screen):
        '''Organizes and enables different views to be intitiated only when needed'''
        self._screen = screen
        self._prev_views = []
        self._current_view = None
        self.setup_views()

    def update(self, events, screen):
        '''Assumes current view is class inheriting from View. Updates current view class.'''
        self._screen = screen
        self._current_view.update(events, screen)

    def switch(self, constructor, *args):
        '''Switches view to given class. Class must be child of view.'''
        self._current_view = self.initiate_new_view(constructor, *args)

    def go_back(self, constructor, *args):
        '''When called by a button for example, switches view to previous view'''
        try:
            self._current_view = self.initiate_new_view(self._prev_views[-1][0], *self._prev_views[-1][1])
            self._prev_views.pop()
        except:
            pass


    def switch_view_callback(self, next_view_constructor, *next_view_args):
        '''Callback wrapper so that callbacks can be passed with arguments without messing things up'''
        def wrapper_func(prev_view_constructor, *prev_view_args):
            '''Function called by button or caller, and class object and parameters must be given to work'''
            self._prev_views.append([prev_view_constructor, *prev_view_args])
            self.switch(next_view_constructor, *next_view_args)
        return wrapper_func

    def initiate_new_view(self, constructor, *args):
        '''Initialize given class with given arguments'''
        return constructor(*args)

    def setup_views(self):

        self._views = {
            'start': (Menu, self._screen, 'middle', 'Start', ('Editor', 'editor_level'), ('Game', 'game_level')),
            'editor_level': (Menu, self._screen, 'left', 'Editor: Pick level to edit.'),
            'editor': None,
            'game': None,
        }
        # Create start menu, with buttons, with callbacks for initiating new views with more buttons and callbacks so on and so forth...
        start_menu = Menu(self._screen, 'middle', 'Start Menu',
            ('Play', self.switch_view_callback(Menu, self._screen, 'left', 'GAME: CHOOSE YOUR LEVEL', *[(level_file, self.switch_view_callback(Game, self._screen, 'lib/data/levels/' + level_file, self.go_back, False)) for level_file in os.listdir('lib/data/levels')], ('Exit', self.go_back))),
            ('Debug Play', self.switch_view_callback(Menu, self._screen, 'left', 'GAME: CHOOSE YOUR LEVEL', *[(level_file, self.switch_view_callback(Game, self._screen, 'lib/data/levels/' + level_file, self.go_back, True)) for level_file in os.listdir('lib/data/levels')], ('Exit', self.go_back))),
            ('Editor', self.switch_view_callback(Menu, self._screen, 'left', 'EDITOR: CHOOSE LEVEL TO EDIT', *[(level_file, self.switch_view_callback(Editor, self._screen, 'lib/data/levels/' + level_file, self.go_back)) for level_file in os.listdir('lib/data/levels')], ('Exit', self.go_back))),
            ('Exit', self.go_back))
        # set start menu as the current_view
        self._current_view = start_menu






def init():


    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('The Game')
    pygame.display.flip()

    return screen



if __name__ == '__main__':
    '''
    Tests
    '''

    import pygame

    screen = init()

    handler = Handler(screen)
    handler.setup_views()
    handler.update(pygame.event.get())

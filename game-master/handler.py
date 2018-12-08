import os

from lib.modules.gui.menu import Menu




class Handler:

    def __init__(self, screen):

        self._views = {}
        self._screen = screen
        self.setup_views()

    def update(self, events):

        if self._current_view.get_visibility():

            self._current_view.update(events)

        else:

            if self._current_view.get_new_view() == 0:

                assert False

            self._current_view = self._views[self._current_view.get_new_view()]
            self._current_view.set_visibility(True)

    def call(self, next_view_id, next_view_arg):

        pass

    def callback(self, next_view_id, next_view_arg):

        def wrapper_func():

            self.call(next_view_id, next_view_arg)

        return wrapper_func()


    def setup_views(self):


        # Start Menu
        Start_Menu = Menu(self._screen, 'middle', 'Start Menu')
        Start_Menu.add_button('Play', 'editor_level_menu')
        Start_Menu.add_button('Editor', 'editor_level_menu')
        Start_Menu.add_button('Settings', 'settings_menu')

        self._views['start_menu'] = Start_Menu

        # Level Menu
        Editor_Level_Menu = Menu(self._screen, 'right', 'Levels')
        for level_file in os.listdir('lib/data/levels'):
            Editor_Level_Menu.add_button(level_file, 'asdf')

        Editor_Level_Menu.add_button('Exit', 'start_menu')
        self._views['editor_level_menu'] = Editor_Level_Menu

        # Settings Menu
        Settings_Menu = Menu(self._screen, 'middle', 'Settings')
        Settings_Menu.add_button('test', 123)
        Settings_Menu.add_button('Exit', 'start_menu')

        self._views['settings_menu'] = Settings_Menu

        # set current view to start menu and turn on visibility
        self._current_view = self._views['start_menu']
        self._current_view.set_visibility(True)

        #Write more code here


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

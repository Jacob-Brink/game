from lib.modules.gui.menu import Menu

class Handler:

    def __init__(self, view, screen)

        self._menus = []
        self._current_view = view
        self._screen

    def change_view(self, new_view_string):
        
        
    def update(events):

        self._current_view.update(events)

    def setup_views(self):

        #Start Menu
        Start_Menu = Menu(self._screen, 'middle', 'Start Menu')
        Start_Menu.add_button('Play', self.change_view('game'))
        Start_Menu.add_button('Editor', self.change_view('level_menu'))
        Start_Menu.add_button('Quit', self.change_view('quit'))

        #Level Menu
        Level_Menu = Menu(self._screen, 'middle', 'Levels')
        #Write more code here

        
    

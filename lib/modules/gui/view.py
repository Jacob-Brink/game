from lib.modules.gui.camera import Camera

class View(Camera):
    def __init__(self, screen, view_rect):
        '''Constructs a view object with given id and view_class. View class must have update function and a switch return that returns next id of view.'''
        super().__init__(view_rect)
        self._screen = screen

    def return_screen_dimensions(self):
        '''Returns screen dimensions of width and height in tuple type'''
        return self._screen.get_width(),self._screen.get_height()

    def camera(self):
        '''returns camera used for placing objects in screen based on absolute positions'''
        return super()

    def render(self, screen, *surfaces):
        '''Given a screen and surfaces, render the surfaces'''
        self._screen = screen
        for surface in surfaces:
            self._screen.blit(surface[0], surface[1])





if __name__ == '__main__':

    from menu import Menu

    m = Menu(1, 'left', 'title', 123)

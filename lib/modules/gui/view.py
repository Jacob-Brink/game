from lib.modules.gui.camera import Camera
import pygame

class View(Camera):
    def __init__(self, screen):
        '''Constructs a view object with given id and view_class. View class must have update function and a switch return that returns next id of view.'''
        super().__init__(screen, (0,0))
        self._screen = screen
        
    def return_screen_dimensions(self):
        '''Returns screen dimensions of width and height in tuple type'''
        return self._screen.get_width(), self._screen.get_height()

    def render_rectangle(self, rect, **keywords):
        '''Given rect with absolute coordinates, draw rectangle'''
        try:
            pygame.draw.rect(self._screen, keywords['color'], super().return_disp_rect(rect))
        except:
            pygame.draw.rect(self._screen, (255,0,0), super().return_disp_rect(rect))
            
    def render_line(self, vector):
        '''Renders a vector with absolute position as a line'''
        pygame.draw.line(self._screen, (200, 100, 240), super().return_display_position(vector.return_start_position()).return_tuple(), super().return_display_position(vector.return_end_position()).return_tuple())
        
    def render(self, screen, *surface_pos):
        '''Given a screen and surfaces, render the surfaces'''
        self._screen = screen

        # renders surface pos types
        for surface in surface_pos:
            self._screen.blit(self.return_display_surface(surface[0]), self.return_display_position(surface[1]).return_tuple())






if __name__ == '__main__':

    from menu import Menu

    m = Menu(1, 'left', 'title', 123)

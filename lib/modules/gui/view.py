from lib.modules.gui.camera import Camera
from lib.modules.gui.rectangle import Point

import pygame

class View(Camera):
    def __init__(self, screen):
        '''Constructs a view object with given id and view_class. View class must have update function and a switch return that returns next id of view.'''
        super().__init__(screen, (0,0))
        self._screen = screen
        
    def return_screen_dimensions(self):
        '''Returns screen dimensions of width and height in tuple type'''
        return Point(self._screen.get_width(), self._screen.get_height())

    def render_rectangle(self, rect, **keywords):
        '''Given rect with absolute coordinates, draw rectangle'''

        if 'color' in keywords:
            pygame.draw.rect(self._screen, keywords['color'], super().return_disp_rect(rect))
        else:
            print(self._screen)
            pygame.draw.rect(self._screen, (255,0,0), super().return_disp_rect(rect))
            
    def render_line(self, vector, **keywords):
        '''Renders a vector with absolute position as a line'''

        if 'relative_screen' in keywords and keywords['relative_screen'] == True:   
            pygame.draw.line(self._screen, (200, 100, 240), vector.return_start_position().return_tuple(), vector.return_end_position().return_tuple())
        else:
            pygame.draw.line(self._screen, (200, 100, 240), super().return_display_position(vector.return_start_position()).return_tuple(), super().return_display_position(vector.return_end_position()).return_tuple())
        
    def render(self, *surface_pos, **keywords):
        '''Given a screen and surfaces, render the surfaces'''
        # renders surface pos types
        for surface in surface_pos:
            if 'relative_screen' in keywords and keywords['relative_screen'] == True:
                self._screen.blit(surface[0], surface[1].return_tuple())
            else:
                self._screen.blit(super().return_display_surface(surface[0]), super().return_display_position(surface[1]).return_tuple())
                
    def update(self, screen):
        '''Updates view screen'''
        print(screen)
        self._screen = screen




if __name__ == '__main__':

    from menu import Menu

    m = Menu(1, 'left', 'title', 123)

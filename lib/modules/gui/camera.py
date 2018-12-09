import pygame
from lib.modules.physics.vector import Vector

def list_rect_points(rect):
    return [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]

def vector_btw_points(point1, point2):
    return Vector(point1, x_component=point2[0]-point1[0], y_component=point2[1]-point1[1])

def interpolate_smooth(start, end, delta_time):
    '''Given start and end position, try to return small steps of movement in a smooth fashion'''
    return Vector(start, x_component=(start[0]-end[0]), y_component=(start[1]-end[1]))
    #add velocity vector to self._view_rect

def return_size(aspect_ratio, **kwrds):
    '''Assumes aspect_ratio is height:width and returns size values given either value'''
    if 'width' in kwrds:
        return kwrds['width'], aspect_ratio * kwrds['width']
    elif 'height' in kwrds:
        return 1/aspect_ratio*kwrds['height'], krwds['height']
    

class Camera:

    def __init__(self, screen, position):
        '''Constructor contructs new camera object determined by the provided viewing rectangle'''
        self._zoom = 1
        self._screen_rect = pygame.Rect((0, 0), screen.get_size())
        self._view_position = position
        self._screen_size = screen.get_size()
        self._aspect_ratio = self._screen_size[1]/self._screen_size[0]
        self._calculate_things()

    def return_camera_position(self):
        return self._view_position
        
    def _calculate_things(self):
        '''Calculate things'''
        view_width = self._screen_rect.width/self._zoom
        view_height = self._screen_rect.height/self._zoom
        view_position_delta = (view_width-self._screen_rect.width)/2, (view_height-self._screen_rect.height)/2
        self._view_position_x = self._view_position[0]-view_position_delta[0]
        self._view_position_y = self._view_position[1]-view_position_delta[1]
        self._view_rect = pygame.Rect((self._view_position_x, self._view_position_y), (view_width, view_height))
        print(self._view_rect)

    def zoom_values(self, *values):
        '''Given any width or height returns the displayed width and height with zoom'''
        return [int(self._zoom*v) for v in values]

    def unzoom_values(self, *values):
        '''Given any number of display widths and heights, returns true widths and heights'''
        return [int(1/self._zoom*v) for v in values]

    def move(self, **kwords):
        '''Public method called to move camera to new location. Note that move does not provide any travel by itself and that the calling code must take this into account.'''
        if 'vector' in kwords:
            self._view_position_x += kwords['vector'].return_x_component()
            self._view_position_y += kwords['vector'].return_y_component()
            #self._view_rect = self._view_rect.move(int(kwords['vector'].return_x_component()), int(kwords['vector'].return_y_component()))
        elif 'change_x' in kwords and 'change_y' in kwords:
            raise Exception('Under construction!')
            #self._view_rect = self._view_rect.move(int(kwords['change_x']), int(kwords['change_y']))
        else:
            raise ValueError('Camera->Move must be given either vector or change_x and change_y')
        print(self._view_rect)
        
    def track(self, rect1, rect2, delta_time):
        '''Resizes camera rect to show both rectangles'''
        #ZOOM
        target_rect = pygame.Rect(rect1.center, rect2.center)
        target_rect.normalize()
            
        #MOVE
        velocity_vector = interpolate_smooth(self._view_rect.center, target_rect.center, delta_time)
        #self.move(vector=velocity_vector)
        #ADD FUNCTIONALITY
        print(velocity_vector)
        

    def update_screen_size(self, screen_size):
        '''Updates screen size to given screen. (Useful for screen resizing and camera adjustment)'''
        self._aspect_ratio = screen_size[1]/screen_size[0]
        self._screen_size = screen_size
        self._calculate_things()

    def zoom(self, magnitude):
        '''Zoom absolutely'''
        self._zoom = magnitude
        self._calculate_things()

    def _true_x_value(self, x_value):
        '''Return true position of disp x value'''
        return (x_value / self._screen_size[0]) * self._view_rect.w + self._view_position[0]+self._view_position_x

    def _true_y_value(self, y_value):
        '''Return true position of disp y value'''
        return (y_value / self._screen_size[1]) * self._view_rect.h + self._view_position[1]+self._view_position_y
        
    def _disp_x_value(self, x_value):
        '''Given value, return screen x in screen offset'''
        return  self._screen_size[0]*(x_value-self._view_position[0]-self._view_position_x)/self._view_rect.w
    
    def _disp_y_value(self, y_value):
        '''Given y_value, return screen y offset'''
        return self._screen_size[1]*(y_value-self._view_position[1]-self._view_position_y)/self._view_rect.h
    def return_display_surface(self, surface):
        '''Given a surface, return the display surface'''
        return pygame.transform.scale(surface, self.zoom_values(*surface.get_size()))
        
    def return_true_position(self, disp_position_tuple):
        '''Returns absolute position of object when given position coordinates of type tuple'''
        return self._true_x_value(disp_position_tuple[0]), self._true_y_value(disp_position_tuple[1])
    
    def return_display_position(self, tru_position_tuple):
        '''Returns display position of given object by returning the difference in coordinates'''
        return self._disp_x_value(tru_position_tuple[0]), self._disp_y_value(tru_position_tuple[1])
    
    def return_true_rect(self, disp_rect):
        '''Returns rectangle with absolute / true positions'''
        return pygame.Rect(self.return_true_position(disp_rect.topleft), self.unzoom_values(*disp_rect.size))

    def return_disp_rect(self, tru_rect):
        '''Returns rectangle with positions relative to window screen'''
        return pygame.Rect(self.return_display_position(tru_rect.topleft), self.zoom_values(*tru_rect.size))

    def is_visible(self, object_rect):
        '''Boolean value of whether given object is in the camera's viewing rectangle. True for is visible and False for invisible.'''
        return object_rect.colliderect(self._view_rect)


if __name__ == '__main__':
    '''
    Tests for camera class.
    '''


    from pygame import Rect

    c = Camera((640, 480), Rect(0, 0, 10, 10))
    r = Rect(0, 0, 20, 10)

    c.zoom(2)

    assert c.return_disp_rect(r).width == 40
    print('Camera tests passed')

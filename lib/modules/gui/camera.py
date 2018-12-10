import pygame
from lib.modules.physics.vector import Vector
from lib.modules.gui.rectangle import *

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
    

class Camera(Rectangle):

    def __init__(self, screen, position):
        '''Constructor contructs new camera object determined by the provided viewing rectangle'''

        self._zoom = 1
        self.ZOOM_MIN = .1
        self.ZOOM_MAX = 2.5

        self._screen_rect = pygame.Rect((0, 0), screen.get_size())
        self._aspect_ratio = self._screen_rect.h/self._screen_rect.w

        # storage of total view position delta from inital start
        self._view_position_delta = Point(0,0)

        self._view_rect = Rectangle(position, screen.get_size())
        
        # recalculate position from screen and zoom
        self._calculate_things()
        
    def return_camera_position(self):
        return self._view_rect.get_top_left()
        
    def _calculate_things(self):
        '''Calculate things'''
        view_width = self._screen_rect.width/self._zoom
        view_height = self._screen_rect.height/self._zoom

        # total delta
        view_position_delta_total = Point((view_width-self._screen_rect.width)/2, (view_height-self._screen_rect.height)/2)
        
        # add recent delta by subtracting the difference between current and past delta totals
        delta_point = Point((-view_position_delta_total.x()+self._view_position_delta.x()), (-view_position_delta_total.y()+self._view_position_delta.y()))
        self._view_rect.move(delta_point)

        # set position_delta total to current total
        self._view_position_delta = view_position_delta_total

        

    def zoom_values(self, *values):
        '''Given any width or height returns the displayed width and height with zoom'''
        return [int(self._zoom*v) for v in values]

    def unzoom_values(self, *values):
        '''Given any number of display widths and heights, returns true widths and heights'''
        return [int(1/self._zoom*v) for v in values]

    def move(self, **kwords):
        '''Public method called to move camera to new location. Note that move does not provide any travel by itself and that the calling code must take this into account.'''

        if 'vector' in kwords:
            delta_point = Point(kwords['vector'].return_x_component(), kwords['vector'].return_y_component())

        elif 'change_x' in kwords and 'change_y' in kwords:
            delta_point = Point(kwords['change_x'], kwords['change_y'])

        else:
            raise ValueError('Camera->Move must be given either vector or change_x and change_y')

        self._view_rect.move(delta_point)
        self._calculate_things()
        
    def track(self, rigid_body1, rigid_body2, delta_time):
        '''Resizes camera rect to show both rectangles'''

        # get average center between two players
        center_1 = rigid_body1.return_rect().get_center()
        center_2 = rigid_body2.return_rect().get_center()
        average_center_target = Point(center_1.x()+(center_2.x()-center_1.x())/2, center_1.y()+(center_2.y()-center_1.y())/2)

        # set camera to center of two players
        self._view_rect.set_center(average_center_target)

        margin = 10

        # calculate zoom necessary for both players to be seen
        # if distance in the x direction is greater, make zoom from width
        if abs(center_1.x() - center_2.x()) > abs(center_1.y() - center_2.y()):
            self.zoom(abs(self._screen_rect.width / (center_1.x() - center_2.x()+margin)))
            pass
        else:
            pass
            self.zoom(abs(self._screen_rect.height / (center_1.y() - center_2.y()+margin)))

        self._calculate_things()
        
    def contains(self, rect1):
        '''Returns boolean state of whether or not a rigid body collided with camera view'''
        return True if self._view_rect.return_pygame_rect().contains(rect1.return_pygame_rect()) == 1 else False
        
    def update_screen_size(self, screen_size):
        '''Updates screen size to given screen. (Useful for screen resizing and camera adjustment)'''
        self._aspect_ratio = screen_size[1]/screen_size[0]
        self._screen_rect.w = screen_size[0]
        self._screen_rect.h = screen_size[1]
        self._calculate_things()

    def zoom(self, magnitude):
        '''Zoom absolutely'''

        if magnitude <= self.ZOOM_MIN:
            self._zoom = self.ZOOM_MIN
            
        elif magnitude > self.ZOOM_MAX:
            self._zoom = self.ZOOM_MAX
            
        else:
            self._zoom = magnitude
            
        self._calculate_things()

    def _true_x_value(self, x_value):
        '''Return true position of disp x value'''
        return x_value/self._zoom +self._view_rect.get_x()

    def _true_y_value(self, y_value):
        '''Return true position of disp y value'''
        return y_value/self._zoom+self._view_rect.get_y()
        
    def _disp_x_value(self, x_value):
        '''Given x value, return screen x in screen offset'''
        return self._zoom*(x_value-self._view_rect.get_x())
    
    def _disp_y_value(self, y_value):
        '''Given y_value, return screen y offset'''
        return self._zoom*(y_value-self._view_rect.get_y())
    
    def return_display_surface(self, surface):
        '''Given a surface, return the display surface'''
        return pygame.transform.scale(surface, self.zoom_values(*surface.get_size()))
        
    def return_true_position(self, disp_position_point):
        '''Returns absolute position of object when given position coordinates of type tuple'''
        return Point(self._true_x_value(disp_position_point.x()), self._true_y_value(disp_position_point.y()))
    
    def return_display_position(self, tru_position_point):
        '''Returns display position of given object by returning the difference in coordinates'''
        return Point(self._disp_x_value(tru_position_point.x()), self._disp_y_value(tru_position_point.y()))
    
    def return_true_rect(self, disp_rect):
        '''Returns rectangle with absolute / true positions from pygame rect'''
        return Rectangle(self.return_true_position(Point(disp_rect.topleft[0], disp_rect.topleft[1])).return_tuple(), self.unzoom_values(*disp_rect.size))

    def return_disp_rect(self, tru_rect):
        '''Returns pygame rectangle with positions relative to window screen'''
        if isinstance(tru_rect, pygame.Rect):
            raise ValueError('Camera requires true rectangle object and returns pygame.rect for display. Argument must be of type Rectangle.')
        return pygame.Rect(self.return_display_position(tru_rect.get_top_left()).return_tuple(), self.zoom_values(*tru_rect.get_size_point().return_tuple()))

    def is_visible(self, object_rect):
        '''Boolean value of whether given object is in the camera's viewing rectangle. True for is visible and False for invisible.'''
        return True if self._view_rect.return_pygame_rect().colliderect(object_rect.return_pygame_rect()) == 1 else False


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

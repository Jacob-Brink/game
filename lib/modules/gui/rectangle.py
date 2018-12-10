import pygame

class Point:
    '''Represents a 2 dimensional point with x and y values'''
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        '''Return x'''
        return self._x
    
    def y(self):
        '''Return y'''
        return self._y
    
    def change_x(self, new_x):
        '''Change x to new_x'''
        self._x = new_x

    def change_y(self, new_y):
        '''Change y to new_y'''
        self._y = new_y

    def change_w(self, new_w):
        '''Change width'''
        self._w = new_w

    def change_h(self, new_h):
        '''Change height'''
        self._h = new_h
        
    def return_tuple(self):
        '''Returns tuple of x and y'''
        return self._x, self._y


    
class Rectangle:

    def check_is_number(self, value):
        '''Returns boolean value of whether or not a value is a value or not'''
        return isinstance(value, int) or isinstance(value, float)
    
    def check_is_nonzero_nonnegative(self, value):
        '''Returns the boolean state of being positive or not'''
        return value > 0

    def list_basic_values(self):
        '''Returns iterable list of values x,y, w, and h'''
        return [self._x, self._y, self._w, self._h]

    def raise_error(self, error):
        '''Raises error wrapper function'''
        raise ValueError(str(error))

    def normalize(self):
        '''When a rectangle has negative width or height, it is corrected for'''
        if self._h < 0:
            self._y += self._h
            self._h = -self._h

        if self._w < 0:
            self._x += self._w
            self._w = -self._w
            
        self.set_values()
    
    '''Rectangle that stores float values unlike pygame.Rect. Models a rectangle'''
    def __init__(self, *args):
        '''Constructs a new rectangle given position tuple and size tuple'''
        
        if isinstance(args[0], tuple) and isinstance(args[1], tuple):
                
                # set four elemental values of rectangle
                self._x = args[0][0]
                self._y = args[0][1]
                
                self._w = args[1][0]
                self._h = args[1][1]

        elif len(args) == 4:
            self._x = args[0]
            self._y = args[1]
            self._w = args[2]
            self._h = args[3]

        else:
            raise ValueError('Either two tuples: one of position one and size, or 4 float or int values of x,y,w, and h')
        
        # check for invariance
        [self.raise_error('Must be integer or float. Got ' + str(value) + ' instead') for value in self.list_basic_values() if not self.check_is_number(value)]
        [self.normalize() for value in [self._w, self._h] if not self.check_is_nonzero_nonnegative(value)]
        
        # set values based on elemental values
        self.set_values()

    def set_values(self):
        '''Sets values based on root values'''

        # set corner points
        self._top_left = Point(self._x, self._y)
        self._top_right = Point(self._x+self._w, self._y)
        self._bottom_left = Point(self._x, self._y+self._h)
        self._bottom_right = Point(self._x+self._w, self._y+self._h)

        # set center
        self._center = Point(self._x+self._w/2, self._y+self._h/2)
    
    def return_pygame_rect(self):
        '''Returns pygame rect for easy blitting and pixel positioning'''
        return pygame.Rect(self._x, self._y, self._w, self._h)

    def scale(self, scale):
        '''Given scale, scale rectangle'''
        # scale width and height
        self._w *= scale
        self._h *= scale

        #maintain same center
        self._x = self._center.x() - self._w / 2
        self._y = self._center.y() - self._h / 2

        # reset values based on x,y,w, and h values
        self.set_values()

    def set_center(self, center_point):
        '''Given center tuple, change center without changing width or height'''
        self._x = center_point.x()-self._w / 2
        self._y = center_point.y()-self._h / 2

        # reset values based on x,y,w, and h values
        self.set_values()
        
    def get_x(self):
        '''Return x'''
        return self._x
    
    def get_y(self):
        '''Return y'''
        return self._y
    
    def get_w(self):
        '''Return w'''
        return self._w
    
    def get_h(self):
        '''Return h'''
        return self._h
    
    def get_center(self):
        '''Return center tuple'''
        return self._center
    
    def get_bottom_left(self):
        '''Return bottom left'''
        return self._bottom_left 

    def get_bottom_right(self):
        '''Return bottom right'''
        return self._bottom_right 

    def get_top_left(self):
        '''Return top left'''
        return self._top_left 

    def get_top_right(self):
        '''Return top right'''
        return self._top_right 

    def change_top_left(self, top_left_point):
        '''Change top left, recalculate corners, and leave width and height alone'''
        self._x = top_left_point.x()
        self._y = top_left_point.y()
        self.set_values()

    def change_top_right(self, top_right_point):
        '''Change top right corner of rectangle'''
        self._x = top_right_point.x()-self._w
        self._y = top_right_point.y()
        self.set_values()

    def change_bottom_left(self, bottom_left_point):
        '''Change bottom right corner of rectangle given point'''
        self._x = bottom_left_point.x()
        self._y = bottom_left_point.y()-self._h
        self.set_values()
        
    def change_bottom_right(self, bottom_right_point):
        '''Change bottom right point'''
        self._x = bottom_right_point.x()-self._w
        self._y = bottom_right_point.y()-self._h
        self.set_values()
        
    def move(self, point_delta):
        '''Moves rectangle position'''
        self._x += point_delta.x()
        self._y += point_delta.y()
        self.set_values()

    def get_size_point(self):
        '''Returns width and height in point form'''
        return Point(self._w, self._h)
        
    def __str__(self):
        '''Return string for pretty print'''
        return str(self._x) + ' ' + str(self._y) + ' ' + str(self._w) + ' ' +str(self._h)

import pygame

class Point:
    '''Represents a 2 dimensional point with x and y values'''
    def check_invariance(self, value):
        '''Raises exception if value is not int or float'''
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError('Point: All values must be type int or float')

    def __init__(self, x, y):
        '''Constructs a point object'''
        self.check_invariance(x)
        self.check_invariance(y)
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
        self.check_invariance(new_x)
        self._x = new_x

    def change_y(self, new_y):
        '''Change y to new_y'''
        self.check_invariance(new_y)
        self._y = new_y
        
    def return_tuple(self):
        '''Returns tuple of x and y'''
        return self._x, self._y

    def __add__(self, other):
        '''Adds two points together by adding x components and then y components'''
        return Point(self._x+other._x, self._y+other._y)

    def __str__(self):
        '''Returns string of points'''
        return str(self._x) + ' ' + str(self._y)

    def __eq__(self, other):
        '''Returns boolean value of whether or not two points are equal to each other'''
        return self._x == other._x and self._y == other._y if isinstance(other, Point) else False
    
    
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

    def list_four_points(self):
        '''Returns iterable list of four corners'''
        return [self._top_left, self._top_right, self._bottom_left, self._bottom_right]
    
    def raise_error(self, error):
        '''Raises error wrapper function'''
        raise ValueError(str(error))

    def copy(self):
        '''Returns a copy of the rectangle'''
        return Rectangle(self.get_top_left().return_tuple(), self.get_size().return_tuple())
    
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

        # if the argument only has two elements, those two elements must be list or tuple type
        if len(args) == 2:

            if isinstance(args[0], Point) and isinstance(args[1], Point):

                self._x = args[0].x()
                self._y = args[0].y()

                self._w = args[1].x()
                self._h = args[1].y()
                
            else:
                # set four elemental values of rectangle
                self._x = args[0][0]
                self._y = args[0][1]
            
                self._w = args[1][0]
                self._h = args[1][1]

        # if the argument has 4 elements, assume they represent x,y,w, and h
        elif len(args) == 4:
            self._x = args[0]
            self._y = args[1]
            self._w = args[2]
            self._h = args[3]

        else:
            raise ValueError('Either two tuples: one of position one and size, or 4 float or int values of x,y,w, and h. Given ' + str(args) + 'instead')
        
        # check for invariance
        [self.raise_error('Must be integer or float. Got ' + str(value) + ' instead') for value in self.list_basic_values() if not self.check_is_number(value)]
        self.normalize()
        
        # set values based on elemental values
        self.set_values()

    def set_values(self):
        '''Sets values based on root values'''

        # ensures any negative widths and heights are changed so space and position are the same but with different heights and widths

        
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

        print(self.get_center())
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

    def get_left(self):
        '''Return left x coordinate'''
        return self._x

    def get_right(self):
        '''Return right x coordinate'''
        return self._x+self._w

    def get_top(self):
        '''Return top y coordinate'''
        return self._y

    def get_bottom(self):
        '''Return bottom y coordinate'''
        return self._y+self._h
    
    def change_top_left(self, top_left_point):
        '''Change top left, recalculate corners, and leave width and height alone'''
        self._x = top_left_point.x()
        self._y = top_left_point.y()
        self.normalize()

    def change_top_right(self, top_right_point):
        '''Change top right corner of rectangle'''
        self._x = top_right_point.x()-self._w
        self._y = top_right_point.y()
        self.normalize()

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

    def change_width(self, new_width):
        '''Changes width to new_width'''
        self._x = self._center.x()-new_width/2
        self._w = new_width
        self.set_values()

    def change_height(self, new_height):
        '''Changes height to new_height'''
        self._y = self._center.y()-new_height/2
        self._h = new_height
        self.set_values()
        
    def get_size(self):
        '''Return size in point form'''
        return Point(self._w, self._h)
    
    def move(self, point_delta):
        '''Moves rectangle position'''
        self._x += point_delta.x()
        self._y += point_delta.y()
        self.set_values()

    def __add__(self, other):
        '''Returns the smallest rectangle that contains both rectangles'''

        dist_centers_x = self._center.x()-other._center.x()
        dist_centers_y = self._center.y()-other._center.y()

        # make a random rectangle for mutating
        r = Rectangle(Point(0,0),Point(1,1))

        # make center average center
        r.set_center(Point(other._center.x()+dist_centers_x/2, other._center.y()+dist_centers_y/2))

        # change size
        r.change_width(abs(dist_centers_x)+self.get_w()/2+other.get_w()/2)
        r.change_height(abs(dist_centers_y)+self.get_h()/2+other.get_h()/2)

        return r
        
    def __str__(self, rounding=True):
        '''Return string for pretty print'''
        return str(round(self._x)) + ' ' + str(round(self._y)) + ' ' + str(round(self._w)) + ' ' +str(round(self._h)) if rounding else  str(self._x) + ' ' + str(self._y) + ' ' + str(self._w) + ' ' +str(self._h)

    def collide_point(self, point):
        '''Returns boolean value of whether or not a point collides with self'''
        if isinstance(point, Point):
            return self.get_x() <= point.x() <= self.get_x() + self.get_w() and self.get_y() <= point.y() <= self.get_y()+self.get_h()
        else:
            raise TypeError('Rectangle->collide_point requires argument to be of type Point')

    def collides_with(self, other):
        '''Returns boolean state of whether or not rectangle collides with any thing else'''
        return self.get_x() <= other.get_x()+other.get_w() and self.get_x()+self.get_w() >= other.get_x() and self.get_y() <= other.get_y()+other.get_h() and self.get_y()+self.get_h() >= other.get_y()

    def __eq__(self, other):
        '''Return boolean value of whether or not rectangles are equal'''
        return self.get_top_left() == other.get_top_left() and self.get_size() == other.get_size() if isinstance(other, Rectangle) else False
